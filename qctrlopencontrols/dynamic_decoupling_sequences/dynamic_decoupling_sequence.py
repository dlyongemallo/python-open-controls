# Copyright 2019 Q-CTRL Pty Ltd & Q-CTRL Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
===================
sequences.sequences
===================
"""

import numpy as np

from qctrlopencontrols.base import QctrlObject
from qctrlopencontrols.exceptions import ArgumentsValueError

from qctrlopencontrols.globals import (
    QCTRL_EXPANDED, CSV, CYLINDRICAL)

from .constants import (UPPER_BOUND_OFFSETS, MATPLOTLIB)
from .driven_controls import convert_dds_to_driven_controls


class DynamicDecouplingSequence(QctrlObject):   #pylint: disable=too-few-public-methods
    """
    Create a dynamic decoupling sequence.
    Can be made of perfect operations, or realistic pulses.

    Parameters
    ----------
    duration : float
        Defaults to 1. The total time in seconds for the sequence.
    offsets : list
        Defaults to None.
        The times offsets in s for the center of pulses.
        If None, defaults to one operation at halfway [0.5].
    rabi_rotations : list
        Default to None.
        The rabi rotations at each time offset.
        If None, defaults to np.pi at each time offset.
    azimuthal_angles : list
        Default to None.
        The azimuthal angles at each time offset.
        If None, defaults to 0 at each time offset.
    detuning_rotations : list
        Default to None.
        The detuning rotations at each time offset.
        If None, defaults to 0 at each time offset.
    pre_post_rotation : bool
        If True, the sequence will have a :math:`X_{\\pi/2}`
        rotations at start (offset=0) and end(offset=duration);
        this will overwrite any operation at the start and the end (if provided).
        If False, it either uses rotations at the start and end (if those are
        supplied) or inserts '0' (no operation) at the start and end
        (if no operation ar those offsets is supplied). Defaults to False.
    name : str
        Name of the sequence; Defaults to None

    Raises
    ------
    qctrlopencontrols.exceptions.ArgumentsValueError
        is raised if one of the inputs is invalid.
    """

    def __init__(self,
                 duration=1.,
                 offsets=None,
                 rabi_rotations=None,
                 azimuthal_angles=None,
                 detuning_rotations=None,
                 pre_post_rotation=False,
                 name=None
                 ):

        super(DynamicDecouplingSequence, self).__init__([
            'duration',
            'offsets',
            'rabi_rotations',
            'azimuthal_angles',
            'detuning_rotations',
            'pre_post_rotation',
            'name'])

        self.duration = duration
        if self.duration <= 0.:
            raise ArgumentsValueError(
                'Sequence duration must be above zero:',
                {'duration': self.duration})

        if offsets is None:
            offsets = [0.5]

        self.offsets = np.array(offsets, dtype=np.float)
        if self.offsets.shape[0] > UPPER_BOUND_OFFSETS:
            raise ArgumentsValueError(
                'Number of offsets is above the allowed number of maximum offsets. ',
                {'number_of_offsets': self.offsets.shape[0],
                 'allowed_maximum_offsets': UPPER_BOUND_OFFSETS})

        if np.any(self.offsets < 0.) or np.any(self.offsets > self.duration):
            raise ArgumentsValueError(
                'Offsets for dynamic decoupling sequence must be between 0 and sequence '
                'duration (inclusive). ',
                {'offsets': offsets,
                 'duration': duration})

        if rabi_rotations is None:
            rabi_rotations = np.pi * np.ones((len(self.offsets),))

        if azimuthal_angles is None:
            azimuthal_angles = np.zeros((len(self.offsets),))

        if detuning_rotations is None:
            detuning_rotations = np.zeros((len(self.offsets),))

        self.rabi_rotations = np.array(rabi_rotations, dtype=np.float)
        self.azimuthal_angles = np.array(azimuthal_angles, dtype=np.float)
        self.detuning_rotations = np.array(detuning_rotations, dtype=np.float)

        self.pre_post_rotation = pre_post_rotation

        if self.offsets[0] != 0.:
            self.offsets = np.append([0], self.offsets)
            if self.pre_post_rotation:
                self.rabi_rotations = np.append([np.pi/2], self.rabi_rotations)
            else:
                self.rabi_rotations = np.append([0], self.rabi_rotations)

            self.azimuthal_angles = np.append([0], self.azimuthal_angles)
            self.detuning_rotations = np.append([0], self.detuning_rotations)
        else:
            if self.pre_post_rotation:
                self.rabi_rotations[0] = np.pi/2

        if self.offsets[-1] != self.duration:
            self.offsets = np.append(self.offsets, [self.duration])
            if self.pre_post_rotation:
                self.rabi_rotations = np.append(self.rabi_rotations, [np.pi/2])
            else:
                self.rabi_rotations = np.append(self.rabi_rotations, [0])

            self.azimuthal_angles = np.append(self.azimuthal_angles, [0])
            self.detuning_rotations = np.append(self.detuning_rotations, [0])
        else:
            if self.pre_post_rotation:
                self.rabi_rotations[-1] = np.pi/2

        self.number_of_offsets = len(self.offsets)

        if len(self.rabi_rotations) != self.number_of_offsets:
            raise ArgumentsValueError(
                'rabi rotations must have the same length as offsets. ',
                {'offsets': offsets,
                 'rabi_rotations': rabi_rotations})

        if len(self.azimuthal_angles) != self.number_of_offsets:
            raise ArgumentsValueError(
                'azimuthal angles must have the same length as offsets. ',
                {'offsets': offsets,
                 'azimuthal_angles': azimuthal_angles})

        if len(self.detuning_rotations) != self.number_of_offsets:
            raise ArgumentsValueError(
                'detuning rotations must have the same length as offsets. ',
                {'offsets': offsets,
                 'detuning_rotations': detuning_rotations,
                 'len(detuning_rotations)': len(self.detuning_rotations),
                 'number_of_offsets': self.number_of_offsets})

        self.name = name
        if self.name is not None:
            self.name = str(self.name)

    def get_plot_formatted_arrays(self, plot_format=MATPLOTLIB):

        """Gets arrays for plotting a pulse.

        Parameters
        ----------
        plot_format : string, optional
            Indicates the format of the plot; Defaults to `matplotlib`

        Returns
        -------
        dict
            A dict with keywords 'rabi_rotations', 'azimuthal_angles',
            'detuning_rotations' and 'times'.

        Raises
        ------
        ArgumentsValueError
            Raised if `plot_format` is not recognized.
        """

        if plot_format != MATPLOTLIB:
            raise ArgumentsValueError("Open Controls currently supports `matplotlib` "
                                      "data format only.",
                                      {'data_format': plot_format})

        offsets = self.offsets
        number_of_offsets = self.number_of_offsets

        plot_data = dict()

        rabi_rotations = self.rabi_rotations
        azimuthal_angles = self.azimuthal_angles
        detuning_rotations = self.detuning_rotations

        rabi_rotations = np.reshape(rabi_rotations, (-1, 1))
        azimuthal_angles = np.reshape(azimuthal_angles, (-1, 1))
        detuning_rotations = np.reshape(detuning_rotations, (-1, 1))

        plot_times = offsets[:, np.newaxis]
        plot_times = np.repeat(plot_times, 3, axis=1)

        multiplier = np.array([0, 1, 0])
        multiplier = multiplier[np.newaxis, :]
        multiplier = np.repeat(multiplier, number_of_offsets, axis=0)
        multiplier = multiplier[np.newaxis, :]

        rabi_rotations = rabi_rotations * multiplier
        azimuthal_angles = azimuthal_angles * multiplier
        detuning_rotations = detuning_rotations * multiplier

        plot_times = plot_times.flatten()
        rabi_rotations = rabi_rotations.flatten()
        azimuthal_angles = azimuthal_angles.flatten()
        detuning_rotations = detuning_rotations.flatten()

        plot_data['rabi_rotations'] = rabi_rotations
        plot_data['azimuthal_angles'] = azimuthal_angles
        plot_data['detuning_rotations'] = detuning_rotations
        plot_data['times'] = plot_times

        return plot_data

    def __str__(self):
        """Prepares a friendly string format for a Dynamic Decoupling Sequence
        """

        dd_sequence_string = list()

        if self.name is not None:
            dd_sequence_string.append('{}:'.format(self.name))

        dd_sequence_string.append('Duration = {}'.format(self.duration))

        pretty_offset = [str(offset/self.duration) for offset in list(self.offsets)]
        pretty_offset = ','.join(pretty_offset)

        dd_sequence_string.append('Offsets = [{}] x {}'.format(pretty_offset, self.duration))

        pretty_rabi_rotations = [
            str(rabi_rotation/np.pi) for rabi_rotation in list(self.rabi_rotations)]
        pretty_rabi_rotations = ','.join(pretty_rabi_rotations)

        dd_sequence_string.append('Rabi Rotations = [{}] x pi'.format(pretty_rabi_rotations))

        pretty_azimuthal_angles = [
            str(azimuthal_angle/np.pi) for azimuthal_angle in list(self.azimuthal_angles)]
        pretty_azimuthal_angles = ','.join(pretty_azimuthal_angles)

        dd_sequence_string.append('Azimuthal Angles = [{}] x pi'.format(pretty_azimuthal_angles))

        pretty_detuning_rotations = [
            str(detuning_rotation/np.pi) for detuning_rotation in list(self.detuning_rotations)]
        pretty_detuning_rotations = ','.join(pretty_detuning_rotations)

        dd_sequence_string.append(
            'Detuning Rotations = [{}] x pi'.format(pretty_detuning_rotations))

        dd_sequence_string = '\n'.join(dd_sequence_string)

        return dd_sequence_string

    def export_to_file(self, filename=None,
                       file_format=QCTRL_EXPANDED,
                       file_type=CSV,
                       coordinates=CYLINDRICAL,
                       maximum_rabi_rate=2*np.pi,
                       maximum_detuning_rate=2*np.pi):

        """Prepares and saves the dynamic decoupling sequence in a file.

        Parameters
        ----------
        filename : str, optional
            Name and path of the file to save the control into.
            Defaults to None
        file_format : str
            Specified file format for saving the control. Defaults to
            'Q-CTRL expanded'; Currently it does not support any other format.
            For detail of the `Q-CTRL Expanded Format` consult
            `Q-CTRL Control Data Format
            <https://docs.q-ctrl.com/output-data-formats#q-ctrl-hardware>` _.
        file_type : str, optional
            One of 'CSV' or 'JSON'; defaults to 'CSV'.
        coordinates : str, optional
            Indicates the co-ordinate system requested. Must be one of
            'Cylindrical', 'Cartesian'; defaults to 'Cylindrical'
        maximum_rabi_rate : float, optional
            Maximum Rabi Rate; Defaults to :math:`2\\pi`
        maximum_detuning_rate : float, optional
            Maximum Detuning Rate; Defaults to :math:`2\\pi`

        References
        ----------
        `Q-CTRL Control Data Format
            <https://docs.q-ctrl.com/output-data-formats#q-ctrl-hardware>` _.

        Raises
        ------
        ArgumentsValueError
            Raised if some of the parameters are invalid.

        Notes
        -----
        The sequence is converted to a driven control using the maximum rabi and detuning
        rate. The driven control is then exported. This is done to facilitate a coherent
        integration with Q-CTRL BLACK OPAL's 1-Qubit workspace.
        """

        driven_control = convert_dds_to_driven_controls(
            dynamic_decoupling_sequence=self,
            maximum_rabi_rate=maximum_rabi_rate,
            maximum_detuning_rate=maximum_detuning_rate,
            name=self.name)

        driven_control.export_to_file(filename=filename,
                                      file_format=file_format,
                                      file_type=file_type,
                                      coordinates=coordinates)


if __name__ == '__main__':
    pass
