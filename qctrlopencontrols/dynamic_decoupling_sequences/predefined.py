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
sequence.predefined
===================
"""

import numpy as np

from qctrlopencontrols.exceptions import ArgumentsValueError


from .constants import (RAMSEY, SPIN_ECHO, CARR_PURCELL,
                        CARR_PURCELL_MEIBOOM_GILL,
                        UHRIG_SINGLE_AXIS,
                        PERIODIC_SINGLE_AXIS,
                        WALSH_SINGLE_AXIS,
                        QUADRATIC,
                        X_CONCATENATED,
                        XY_CONCATENATED)

from .dynamic_decoupling_sequence import DynamicDecouplingSequence


def new_predefined_dds(scheme=SPIN_ECHO, **kwargs):

    """Create a new instance of ne of the predefined
    dynamic decoupling sequence

    Parameters
    ----------
    scheme : string
        The name of the sequence; Defaults to 'Spin echo'
        Available options are,
        - 'Ramsey'
        - 'Spin echo',
        - 'Carr-Purcell',
        - 'Carr-Purcell-Meiboom-Gill',
        - 'Uhrig single-axis'
        - 'Periodic single-axis'
        - 'Walsh single-axis'
        - 'Quadratic'
        - 'X concatenated'
        - 'XY concatenated'
    kwargs : dict, optional
        Additional keyword argument to create the sequence

    Returns
    ------
    qctrlopencontrols.sequences.DynamicDecouplingSequence
        Returns a sequence corresponding to the name

    Raises
    -----
    ArgumentsValueError
        Raised when an argument is invalid.
    """

    if scheme == RAMSEY:
        sequence = new_ramsey_sequence(**kwargs)
    elif scheme == SPIN_ECHO:
        sequence = new_spin_echo_sequence(**kwargs)
    elif scheme == CARR_PURCELL:
        sequence = new_carr_purcell_sequence(**kwargs)
    elif scheme == CARR_PURCELL_MEIBOOM_GILL:
        sequence = new_carr_purcell_meiboom_gill_sequence(**kwargs)
    elif scheme == UHRIG_SINGLE_AXIS:
        sequence = new_uhrig_single_axis_sequence(**kwargs)
    elif scheme == PERIODIC_SINGLE_AXIS:
        sequence = new_periodic_single_axis_sequence(**kwargs)
    elif scheme == WALSH_SINGLE_AXIS:
        sequence = new_walsh_single_axis_sequence(**kwargs)
    elif scheme == QUADRATIC:
        sequence = new_quadratic_sequence(**kwargs)
    elif scheme == X_CONCATENATED:
        sequence = new_x_concatenated_sequence(**kwargs)
    elif scheme == XY_CONCATENATED:
        sequence = new_xy_concatenated_sequence(**kwargs)
    # Raise an error if the input sequence is not known
    else:
        raise ArgumentsValueError(
            'Unknown predefined sequence scheme. Allowed schemes are: '
            + ', '.join([RAMSEY, SPIN_ECHO, CARR_PURCELL,
                         CARR_PURCELL_MEIBOOM_GILL,
                         UHRIG_SINGLE_AXIS,
                         PERIODIC_SINGLE_AXIS,
                         WALSH_SINGLE_AXIS,
                         QUADRATIC,
                         X_CONCATENATED,
                         XY_CONCATENATED]) + '.',
            {'sequence_name': scheme})

    return sequence


def new_ramsey_sequence(duration=None, **kwargs):

    """Ramsey sequence

    Parameters
    ----------
    duration : float, optional
        Total duration of the sequence. Defaults to None
    kwargs : dict
        Additional keywords required by
        qctrlopencontrols.sequences.DynamicDecouplingSequence

    Returns
    -------
    qctrlopencontrols.sequence.DynamicDecouplingSequence
        The Ramsey sequence

    Raises
    ------
    ArgumentsValueError
        Raised when an argument is invalid.

    """
    if duration is None:
        duration = 1.
    if duration <= 0.:
        raise ArgumentsValueError(
            'Sequence duration must be above zero:',
            {'duration': duration})

    offsets = np.array([0.0, duration])
    rabi_rotations = np.zeros(offsets.shape)
    azimuthal_angles = np.zeros(offsets.shape)
    detuning_rotations = np.zeros(offsets.shape)

    return DynamicDecouplingSequence(
        duration=duration, offsets=offsets,
        rabi_rotations=rabi_rotations,
        azimuthal_angles=azimuthal_angles,
        detuning_rotations=detuning_rotations,
        **kwargs)


def new_spin_echo_sequence(duration=None, **kwargs):

    """Spin Echo Sequence.

    Parameters
    ---------
    duration : float, optional
        Total duration of the sequence. Defaults to None
    kwargs : dict
        Additional keywords required by
        qctrlopencontrols.sequences.DynamicDecouplingSequence

    Returns
    -------
    qctrlopencontrols.sequences.DynamicDecouplingSequence
        Spin echo sequence

    Raises
    ------
    ArgumentsValueError
        Raised when an argument is invalid.
    """

    if duration is None:
        duration = 1.
    if duration <= 0.:
        raise ArgumentsValueError(
            'Sequence duration must be above zero:',
            {'duration': duration})

    offsets = duration * np.array([0.5])
    rabi_rotations = np.array([np.pi])
    azimuthal_angles = np.zeros(offsets.shape)
    detuning_rotations = np.zeros(offsets.shape)

    return DynamicDecouplingSequence(
        duration=duration, offsets=offsets,
        rabi_rotations=rabi_rotations,
        azimuthal_angles=azimuthal_angles,
        detuning_rotations=detuning_rotations,
        **kwargs)


def new_carr_purcell_sequence(duration=None, number_of_offsets=None, **kwargs):

    """Carr-Purcell Sequence.

    Parameters
    ---------
    duration : float, optional
        Total duration of the sequence. Defaults to None
    number_of_offsets : int, optional
        Number of offsets. Defaults to None
    kwargs : dict
        Additional keywords required by
        qctrlopencontrols.sequences.DynamicDecouplingSequence

    Returns
    -------
    qctrlopencontrols.sequences.DynamicDecouplingSequence
        Carr-Purcell sequence

    Raises
    ------
    ArgumentsValueError
        Raised when an argument is invalid.
    """
    if duration is None:
        duration = 1.
    if duration <= 0.:
        raise ArgumentsValueError(
            'Sequence duration must be above zero:',
            {'duration': duration})

    if number_of_offsets is None:
        number_of_offsets = 1
    number_of_offsets = int(number_of_offsets)
    if number_of_offsets <= 0.:
        raise ArgumentsValueError(
            'Number of offsets must be above zero:',
            {'number_of_offsets': number_of_offsets})

    offsets = _carr_purcell_meiboom_gill_offsets(duration, number_of_offsets)
    rabi_rotations = np.zeros(offsets.shape)
    azimuthal_angles = np.zeros(offsets.shape)
    detuning_rotations = np.zeros(offsets.shape)

    # set all as X_pi
    rabi_rotations[0:] = np.pi

    return DynamicDecouplingSequence(
        duration=duration, offsets=offsets,
        rabi_rotations=rabi_rotations, azimuthal_angles=azimuthal_angles,
        detuning_rotations=detuning_rotations, **kwargs)


def new_carr_purcell_meiboom_gill_sequence(duration=None,  # pylint: disable=invalid-name
                                           number_of_offsets=None,
                                           **kwargs):
    """Carr-Purcell-Meiboom-Gill Sequences.

    Parameters
    ---------
    duration : float
        Total duration of the sequence. Defaults to None
    number_of_offsets : int, optional
        Number of offsets. Defaults to None
    kwargs : dict
        Additional keywords required by
        qctrlopencontrols.sequences.DynamicDecouplingSequence

    Returns
    -------
    qctrlopencontrols.sequences.DynamicDecouplingSequence
        Carr-Purcell-Meiboom-Gill sequence

    Raises
    ------
    ArgumentsValueError
        Raised when an argument is invalid.
    """
    if duration is None:
        duration = 1.
    if duration <= 0.:
        raise ArgumentsValueError(
            'Sequence duration must be above zero:',
            {'duration': duration})

    if number_of_offsets is None:
        number_of_offsets = 1
    number_of_offsets = int(number_of_offsets)
    if number_of_offsets <= 0.:
        raise ArgumentsValueError(
            'Number of offsets must be above zero:',
            {'number_of_offsets': number_of_offsets})

    offsets = _carr_purcell_meiboom_gill_offsets(duration, number_of_offsets)

    rabi_rotations = np.zeros(offsets.shape)
    azimuthal_angles = np.zeros(offsets.shape)
    detuning_rotations = np.zeros(offsets.shape)

    # set all azimuthal_angles=pi/2, rabi_rotations = pi
    rabi_rotations[0:] = np.pi
    azimuthal_angles[0:] = np.pi/2

    return DynamicDecouplingSequence(
        duration=duration, offsets=offsets,
        rabi_rotations=rabi_rotations,
        azimuthal_angles=azimuthal_angles,
        detuning_rotations=detuning_rotations,
        **kwargs)


def new_uhrig_single_axis_sequence(duration=None, number_of_offsets=None, **kwargs):

    """Uhrig Single Axis Sequence.

    Parameters
    ---------
    duration : float
        Total duration of the sequence. Defaults to None
    number_of_offsets : int, optional
        Number of offsets. Defaults to None
    kwargs : dict
        Additional keywords required by
        qctrlopencontrols.sequences.DynamicDecouplingSequence

    Returns
    -------
    qctrlopencontrols.sequences.DynamicDecouplingSequence
        Uhrig (single-axis) sequence

    Raises
    ------
    ArgumentsValueError
        Raised when an argument is invalid.
    """
    if duration is None:
        duration = 1.
    if duration <= 0.:
        raise ArgumentsValueError(
            'Sequence duration must be above zero:',
            {'duration': duration})

    if number_of_offsets is None:
        number_of_offsets = 1
    number_of_offsets = int(number_of_offsets)
    if number_of_offsets <= 0.:
        raise ArgumentsValueError(
            'Number of offsets must be above zero:',
            {'number_of_offsets': number_of_offsets})

    offsets = _uhrig_single_axis_offsets(duration, number_of_offsets)

    rabi_rotations = np.zeros(offsets.shape)
    azimuthal_angles = np.zeros(offsets.shape)
    detuning_rotations = np.zeros(offsets.shape)

    # set all the azimuthal_angles as pi/2, rabi_rotations = pi
    rabi_rotations[0:] = np.pi
    azimuthal_angles[0:] = np.pi/2

    return DynamicDecouplingSequence(
        duration=duration, offsets=offsets,
        rabi_rotations=rabi_rotations,
        azimuthal_angles=azimuthal_angles,
        detuning_rotations=detuning_rotations,
        **kwargs)


def new_periodic_single_axis_sequence(duration=None,    # pylint: disable=invalid-name
                                      number_of_offsets=None, **kwargs):

    """Periodic Single Axis Sequence.

    Parameters
    ---------
    duration : float
        Total duration of the sequence. Defaults to None
    number_of_offsets : int, optional
        Number of offsets. Defaults to None
    kwargs : dict
        Additional keywords required by
        qctrlopencontrols.sequences.DynamicDecouplingSequence

    Returns
    -------
    qctrlopencontrols.sequences.DynamicDecouplingSequence
        Periodic (single-axis) sequence

    Raises
    ------
    ArgumentsValueError
        Raised when an argument is invalid.
    """
    if duration is None:
        duration = 1.
    if duration <= 0.:
        raise ArgumentsValueError(
            'Sequence duration must be above zero:',
            {'duration': duration})

    if number_of_offsets is None:
        number_of_offsets = 1
    number_of_offsets = int(number_of_offsets)
    if number_of_offsets <= 0.:
        raise ArgumentsValueError(
            'Number of offsets must be above zero:',
            {'number_of_offsets': number_of_offsets})

    spacing = 1./(number_of_offsets+1)
    # prepare the offsets for delta comb
    deltas = [k*spacing for k in range(1, number_of_offsets+1)]
    deltas = np.array(deltas)
    offsets = duration * deltas

    rabi_rotations = np.zeros(offsets.shape)
    azimuthal_angles = np.zeros(offsets.shape)
    detuning_rotations = np.zeros(offsets.shape)

    # set all the rabi_rotations to X_pi
    rabi_rotations[0:] = np.pi

    return DynamicDecouplingSequence(
        duration=duration, offsets=offsets,
        rabi_rotations=rabi_rotations,
        azimuthal_angles=azimuthal_angles,
        detuning_rotations=detuning_rotations,
        **kwargs)


def new_walsh_single_axis_sequence(duration=None,
                                   paley_order=None,
                                   **kwargs):

    """Welsh Single Axis Sequence.

    Parameters
    ---------
    duration : float
        Total duration of the sequence. Defaults to None
    paley_order : int, optional
        Defaults to 1. The paley order of the walsh sequence.
    kwargs : dict
        Additional keywords required by
        qctrlopencontrols.sequences.DynamicDecouplingSequence

    Returns
    -------
    qctrlopencontrols.sequences.DynamicDecouplingSequence
        Walsh (single-axis) sequence

    Raises
    ------
    ArgumentsValueError
        Raised when an argument is invalid.
    """
    if duration is None:
        duration = 1.
    if duration <= 0.:
        raise ArgumentsValueError(
            'Sequence duration must be above zero:',
            {'duration': duration})

    if paley_order is None:
        paley_order = 1
    paley_order = int(paley_order)
    if paley_order < 1 or paley_order > 2000:
        raise ArgumentsValueError(
            'Paley order must be between 1 and 2000.',
            {'paley_order': paley_order})

    hamming_weight = int(np.floor(np.log2(paley_order))) + 1

    samples = 2 ** hamming_weight

    relative_offset = np.arange(1. / (2 * samples), 1., 1. / samples)

    binary_string = np.binary_repr(paley_order)
    binary_order = [int(binary_string[i]) for i in range(hamming_weight)]
    walsh_array = np.ones([samples])
    for i in range(hamming_weight):
        walsh_array *= np.sign(np.sin(2 ** (i + 1) * np.pi
                                      * relative_offset)) ** binary_order[hamming_weight - 1 - i]

    walsh_relative_offsets = []
    for i in range(samples - 1):
        if walsh_array[i] != walsh_array[i + 1]:
            walsh_relative_offsets.append((i + 1) * (1. / samples))
    walsh_relative_offsets = np.array(walsh_relative_offsets, dtype=np.float)
    offsets = duration * walsh_relative_offsets

    rabi_rotations = np.zeros(offsets.shape)
    azimuthal_angles = np.zeros(offsets.shape)
    detuning_rotations = np.zeros(offsets.shape)

    # set the rabi_rotations to X_pi
    rabi_rotations[0:] = np.pi

    return DynamicDecouplingSequence(
        duration=duration, offsets=offsets,
        rabi_rotations=rabi_rotations,
        azimuthal_angles=azimuthal_angles,
        detuning_rotations=detuning_rotations,
        **kwargs)


def new_quadratic_sequence(duration=None,
                           number_inner_offsets=None, number_outer_offsets=None,
                           **kwargs):

    """Quadratic Decoupling Sequence

    Parameters
    ----------
    duration : float, optional
        defaults to None
        The total duration of the sequence
    number_outer_offsets : int, optional
        Number of outer X-pi Pulses. Defaults to None. Not used if number_of_offsets
        is supplied.
    number_inner_offsets : int, optional
        Number of inner Z-pi Pulses. Defaults to None. Not used if number_of_offsets
        is supplied
    kwargs : dict
        Additional keywords required by
        qctrlopencontrols.sequences.DynamicDecouplingSequence

    Returns
    -------
    qctrlopencontrols.sequences.DynamicDecouplingSequence
        Quadratic sequence

    Raises
    ------
    ArgumentsValueError
        Raised when an argument is invalid.
    """

    if duration is None:
        duration = 1.
    if duration <= 0.:
        raise ArgumentsValueError(
            'Sequence duration must be above zero:',
            {'duration': duration})

    if number_inner_offsets is None:
        number_inner_offsets = 1
    number_inner_offsets = int(number_inner_offsets)
    if number_inner_offsets <= 0.:
        raise ArgumentsValueError(
            'Number of offsets of inner pulses must be above zero:',
            {'number_inner_offsets': number_inner_offsets},
            extras={'duration': duration, 'number_outer_offsets': number_outer_offsets})

    if number_outer_offsets is None:
        number_outer_offsets = 1
    number_outer_offsets = int(number_outer_offsets)
    if number_outer_offsets <= 0.:
        raise ArgumentsValueError(
            'Number of offsets of outer pulses must be above zero:',
            {'number_inner_offsets': number_outer_offsets},
            extras={'duration': duration, 'number_inner_offsets': number_inner_offsets})

    outer_offsets = _uhrig_single_axis_offsets(duration, number_outer_offsets)
    outer_offsets = np.insert(outer_offsets, [0, outer_offsets.shape[0]], [0, duration])
    starts = outer_offsets[0:-1]
    ends = outer_offsets[1:]
    inner_durations = ends - starts

    # inner_offsets = np.zeros((number_outer_offsets + 1, number_inner_offsets))
    offsets = np.zeros((inner_durations.shape[0], number_inner_offsets + 1))
    for inner_duration_idx in range(inner_durations.shape[0]):
        inn_off = _uhrig_single_axis_offsets(inner_durations[inner_duration_idx],
                                             number_inner_offsets)
        inn_off = inn_off + starts[inner_duration_idx]
        offsets[inner_duration_idx, 0:number_inner_offsets] = inn_off
    offsets[0:number_outer_offsets, -1] = outer_offsets[1:-1]

    rabi_rotations = np.zeros(offsets.shape)
    detuning_rotations = np.zeros(offsets.shape)

    rabi_rotations[0:number_outer_offsets, -1] = np.pi
    detuning_rotations[0:(number_outer_offsets + 1), 0:number_inner_offsets] = np.pi

    # make all the arrays 1D;
    offsets = np.reshape(offsets, (-1,))
    rabi_rotations = np.reshape(rabi_rotations, (-1,))
    detuning_rotations = np.reshape(detuning_rotations, (-1,))

    # remove the last entry corresponding to the duration
    offsets = offsets[0:-1]
    rabi_rotations = rabi_rotations[0:-1]
    detuning_rotations = detuning_rotations[0:-1]

    # finally create the azimuthal angles as all zeros
    azimuthal_angles = np.zeros(offsets.shape)

    return DynamicDecouplingSequence(
        duration=duration, offsets=offsets,
        rabi_rotations=rabi_rotations,
        azimuthal_angles=azimuthal_angles,
        detuning_rotations=detuning_rotations,
        **kwargs)


def new_x_concatenated_sequence(duration=1.0, concatenation_order=None, **kwargs):

    """X-Concatenated Dynamic Decoupling Sequence
    Concatenation of base sequence C(\tau/2)XC(\tau/2)X

    Parameters
    ----------
    duration : float, optional
        defaults to None
        The total duration of the sequence
    concatenation_order : int, optional
        defaults to None
        The number of concatenation of base sequence
    kwargs : dict
        Additional keywords required by
        qctrlopencontrols.sequences.DynamicDecouplingSequence

    Returns
    -------
    qctrlopencontrols.sequences.DynamicDecouplingSequence
        X concatenated sequence

    Raises
    ------
    ArgumentsValueError
        Raised when an argument is invalid.
    """
    if duration is None:
        duration = 1.
    if duration <= 0.:
        raise ArgumentsValueError(
            'Sequence duration must be above zero:',
            {'duration': duration})

    if concatenation_order is None:
        concatenation_order = 1
    concatenation_order = int(concatenation_order)
    if concatenation_order <= 0.:
        raise ArgumentsValueError(
            'Concatenation oder must be above zero:',
            {'concatenation_order': concatenation_order},
            extras={'duration': duration})

    unit_spacing = duration / (2 ** concatenation_order)
    cumulations = _concatenation_x(concatenation_order)

    pos_cum = cumulations * unit_spacing
    pos_cum_sum = np.cumsum(pos_cum)

    values, counts = np.unique(pos_cum_sum, return_counts=True)

    offsets = [values[i] for i in range(counts.shape[0]) if counts[i] % 2 == 0]

    if concatenation_order % 2 == 1:
        offsets = offsets[0:-1]

    offsets = np.array(offsets)

    rabi_rotations = np.pi * np.ones(offsets.shape)
    azimuthal_angles = np.zeros(offsets.shape)
    detuning_rotations = np.zeros(offsets.shape)

    return DynamicDecouplingSequence(
        duration=duration, offsets=offsets,
        rabi_rotations=rabi_rotations,
        azimuthal_angles=azimuthal_angles,
        detuning_rotations=detuning_rotations,
        **kwargs)


def new_xy_concatenated_sequence(duration=1.0, concatenation_order=None, **kwargs):

    """XY-Concatenated Dynamic Decoupling Sequence
    Concatenation of base sequence C(\tau/4)XC(\tau/4)YC(\tau/4)XC(\tau/4)Y

    Parameters
    ----------
    duration : float, optional
        defaults to None
        The total duration of the sequence
    concatenation_order : int, optional
        defaults to None
        The number of concatenation of base sequence
    kwargs : dict
        Additional keywords required by
        qctrlopencontrols.sequences.DynamicDecouplingSequence

    Returns
    -------
    qctrlopencontrols.sequences.DynamicDecouplingSequence
        XY concatenated sequence

    Raises
    ------
    ArgumentsValueError
        Raised when an argument is invalid.
    """
    if duration is None:
        duration = 1.
    if duration <= 0.:
        raise ArgumentsValueError(
            'Sequence duration must be above zero:',
            {'duration': duration})

    if concatenation_order is None:
        concatenation_order = 1
    concatenation_order = int(concatenation_order)
    if concatenation_order <= 0.:
        raise ArgumentsValueError(
            'Concatenation oder must be above zero:',
            {'concatenation_order': concatenation_order},
            extras={'duration': duration})

    unit_spacing = duration / (2 ** (concatenation_order*2))
    cumulations = _concatenation_xy(concatenation_order)

    rabi_operations = cumulations[cumulations != -2]
    rabi_operations = rabi_operations[rabi_operations != -3]
    rabi_positions = np.zeros(rabi_operations.shape)
    rabi_positions[rabi_operations != -1] = 1
    rabi_positions = rabi_positions * unit_spacing
    rabi_positions = np.cumsum(rabi_positions)

    values, counts = np.unique(rabi_positions, return_counts=True)
    rabi_offsets = [values[i] for i in range(counts.shape[0]) if counts[i] % 2 == 0]

    azimuthal_operations = cumulations[cumulations != -1]
    azimuthal_operations = azimuthal_operations[azimuthal_operations != -3]
    azimuthal_positions = np.zeros(azimuthal_operations.shape)
    azimuthal_positions[azimuthal_operations != -2] = 1
    azimuthal_positions = azimuthal_positions * unit_spacing
    azimuthal_positions = np.cumsum(azimuthal_positions)

    values, counts = np.unique(azimuthal_positions, return_counts=True)
    azimuthal_offsets = [values[i] for i in range(counts.shape[0]) if counts[i] % 2 == 0]

    detuning_operations = cumulations[cumulations != -2]
    detuning_operations = detuning_operations[detuning_operations != -1]
    detuning_positions = np.zeros(detuning_operations.shape)
    detuning_positions[detuning_operations != -3] = 1
    detuning_positions = detuning_positions * unit_spacing
    detuning_positions = np.cumsum(detuning_positions)

    values, counts = np.unique(detuning_positions, return_counts=True)
    detuning_offsets = [values[i] for i in range(counts.shape[0]) if counts[i] % 2 == 0]

    # right now we have got all the offset positions separately; now have
    # put then all together

    offsets = np.zeros((len(rabi_offsets) + len(azimuthal_offsets) + len(detuning_offsets),))

    rabi_rotations = np.zeros(offsets.shape)
    azimuthal_angles = np.zeros(offsets.shape)
    detuning_rotations = np.zeros(offsets.shape)

    rabi_idx = 0
    azimuthal_idx = 0

    carr_idx = 0
    while (rabi_idx < len(rabi_offsets) and
           azimuthal_idx < len(azimuthal_offsets)):

        if rabi_offsets[rabi_idx] < azimuthal_offsets[azimuthal_idx]:
            rabi_rotations[carr_idx] = np.pi
            offsets[carr_idx] = rabi_offsets[rabi_idx]
            rabi_idx += 1
        else:
            azimuthal_angles[carr_idx] = np.pi / 2
            rabi_rotations[carr_idx] = np.pi
            offsets[carr_idx] = azimuthal_offsets[azimuthal_idx]
            azimuthal_idx += 1
        carr_idx += 1

    if rabi_idx < len(rabi_offsets):

        while rabi_idx < len(rabi_offsets):
            rabi_rotations[carr_idx] = np.pi
            offsets[carr_idx] = rabi_offsets[rabi_idx]
            carr_idx += 1
            rabi_idx += 1
    if azimuthal_idx < len(azimuthal_offsets):
        while azimuthal_idx < len(azimuthal_offsets):
            azimuthal_angles[carr_idx] = np.pi / 2
            rabi_rotations[carr_idx] = np.pi
            offsets[carr_idx] = azimuthal_offsets[azimuthal_idx]
            carr_idx += 1
            azimuthal_idx += 1

    # if there is any z-offset, add those too !!!
    if detuning_offsets:
        z_idx = 0
        for carr_idx, offset in enumerate(offsets):
            if offset > detuning_offsets[z_idx]:
                offsets[carr_idx + 1:] = offsets[carr_idx:-1]
                rabi_rotations[carr_idx + 1:] = rabi_rotations[carr_idx:-1]
                azimuthal_angles[carr_idx + 1:] = azimuthal_angles[carr_idx:-1]
                detuning_rotations[carr_idx] = np.pi
                rabi_rotations[carr_idx] = 0
                azimuthal_angles[carr_idx] = 0
                offsets[carr_idx] = detuning_offsets[z_idx]
                z_idx += 1
            if z_idx >= len(detuning_offsets):
                break

    return DynamicDecouplingSequence(
        duration=duration, offsets=offsets,
        rabi_rotations=rabi_rotations,
        azimuthal_angles=azimuthal_angles,
        detuning_rotations=detuning_rotations,
        **kwargs)


def _carr_purcell_meiboom_gill_offsets(duration=1.0, number_of_offsets=1):

    """Offset values for Carr-Purcell_Meiboom-Gill sequence.

    Parameters
    ----------
    duration : float, optional
        Duration of the total sequence; defaults to 1.0
    number_of_offsets : int, optional
        The number of offsets; defaults to 1

    Returns
    ------
    numpy.ndarray
        The offset values
    """

    spacing = 1./number_of_offsets
    start = spacing * 0.5

    # prepare the offsets for delta comb
    deltas = spacing * np.arange(number_of_offsets)
    deltas += start

    offsets = deltas * duration

    return offsets


def _uhrig_single_axis_offsets(duration=1.0, number_of_offsets=1):

    """Offset values for Uhrig Single Axis Sequence.

    Parameters
    ----------
    duration : float, optional
        Duration of the total sequence; defaults to 1.0
    number_of_offsets : int, optional
        The number of offsets; defaults to 1

    Returns
    ------
    numpy.ndarray
        The offset values
    """

    # prepare the offsets for delta comb
    constant = 1./(2*number_of_offsets+2)
    deltas = [(np.sin(np.pi * k * constant)) ** 2 for k in range(1, number_of_offsets+1)]
    deltas = np.array(deltas)

    offsets = duration * deltas

    return offsets


def _concatenation_x(concatenation_sequence=1):

    """Private function to prepare the sequence of operations for x-concatenated
    dynamical decoupling sequence

    Parameters
    ----------
    concatenation_sequence : int, optional
        Duration of the total sequence; defaults to 1

    Returns
    ------
    numpy.ndarray
        The offset values
    """

    if concatenation_sequence == 1:
        return np.array([1, 0, 1, 0])

    cumulated_operations = np.concatenate(
        (_concatenation_x(concatenation_sequence - 1), np.array([0]),
         _concatenation_x(concatenation_sequence - 1), np.array([0])), axis=0)
    return cumulated_operations


def _concatenation_xy(concatenation_sequence=1):

    """Private function to prepare the sequence of operations for x-concatenated
    dynamical decoupling sequence

    Parameters
    ----------
    concatenation_sequence : int, optional
        Duration of the total sequence; defaults to 1

    Returns
    ------
    numpy.ndarray
        The offset values
    """

    if concatenation_sequence == 1:
        return np.array([1, -1, 1, -2, 1, -1, 1, -2])
    cumulations = np.concatenate((_concatenation_xy(concatenation_sequence - 1),
                                  np.array([-1])), axis=0)
    cumulations = cumulations[0:-1]
    cumulations[-1] = -3
    cumulations = np.concatenate((cumulations, _concatenation_xy(concatenation_sequence - 1),
                                  np.array([-2])), axis=0)
    cumulations = cumulations[0:-2]
    cumulations = np.concatenate((cumulations, _concatenation_xy(concatenation_sequence - 1),
                                  np.array([-1])), axis=0)
    cumulations = cumulations[0:-1]
    cumulations[-1] = -3
    cumulations = np.concatenate((cumulations, _concatenation_xy(concatenation_sequence - 1),
                                  np.array([-2])), axis=0)
    if cumulations[-1] == -2 and cumulations[-2] == -2:
        cumulations = cumulations[0:-2]
    return cumulations


if __name__ == '__main__':
    pass
