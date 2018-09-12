from spinn_utilities.overrides import overrides
from pacman.executor.injection_decorator import inject_items
from spynnaker.pyNN.models.neural_properties import NeuronParameter
from .neuron_model_leaky_integrate import NeuronModelLeakyIntegrate

from data_specification.enums import DataType

import numpy
from enum import Enum


V_RESET = "v_reset"
TAU_REFRAC = "tau_refrac"
COUNTDOWN_TO_REFRACTORY_PERIOD = "countdown_to_refactory_period"
V_PREV = "v_prev"
V_SLOW = "v_slow"
DV_DT_S = "dv_dt_slow"
TAU_LP = "tau_low_pass"
GAMMA = "gamma"
GAMMA_COMP = "gamma_complement"
V_MAX = "v_max"
V_SPIKE = "v_spike"
V_NMDA = "v_nmda"
_CPU_RESET_CYCLES = 20  # pure guesswork
_CPU_SPIKE_CYCLES = 10

NUM_EXTRA_PARAMS = 11
class _LIF_DV_TYPES(Enum):
    REFRACT_COUNT = (1, DataType.INT32)
    V_RESET = (2, DataType.S1615)
    TAU_REFRACT = (3, DataType.INT32)
    V_PREV = (4, DataType.S1615)
    V_SLOW = (5, DataType.S1615)
    DV_DT_SLOW = (6, DataType.S1615)
    GAMMA = (7, DataType.S1615) # history weight for slow dV/dt
    GAMMA_COMP = (8, DataType.S1615)  # 1 - GAMMA
    V_MAX = (9, DataType.S1615)
    V_SPIKE = (10, DataType.S1615)
    V_NMDA = (11, DataType.S1615)

    def __new__(cls, value, data_type, doc=""):
        # pylint: disable=protected-access
        obj = object.__new__(cls)
        obj._value_ = value
        obj._data_type = data_type
        obj.__doc__ = doc
        return obj

    @property
    def data_type(self):
        return self._data_type


class NeuronModelLeakyIntegrateAndFireDvDtNMDA(NeuronModelLeakyIntegrate):
    __slots__ = [
        "_my_units"]

    def __init__(
            self, n_neurons, v_init, v_rest, tau_m, cm, i_offset, v_reset,
            tau_refrac, tau_low_pass, v_max=-28.0, v_spike=-30.0, v_nmda=0.):
        # pylint: disable=too-many-arguments
        super(NeuronModelLeakyIntegrateAndFireDvDtNMDA, self).__init__(
            n_neurons, v_init, v_rest, tau_m, cm, i_offset)
        self._data[V_RESET] = v_reset
        self._data[TAU_REFRAC] = tau_refrac
        self._data[COUNTDOWN_TO_REFRACTORY_PERIOD] = 0
        self._data[V_PREV] = v_rest
        self._data[V_SLOW] = v_rest
        self._data[DV_DT_S] = 0
        self._data[TAU_LP] = tau_low_pass
        gamma = numpy.exp(-1.0/tau_low_pass)
        self._data[GAMMA] = gamma
        self._data[GAMMA_COMP] = 1. - gamma
        self._data[V_MAX] = v_max
        self._data[V_SPIKE] = v_spike
        self._data[V_NMDA] = v_nmda
        self._my_units = {
            V_RESET: 'mV', V_PREV: 'mV', 
            TAU_REFRAC: 'ms', TAU_LP: 'ms',
            V_SLOW: 'mV', DV_DT_S: 'mV/ms',
            V_MAX: 'mV', V_SPIKE: 'mV',
            V_NMDA: 'mV',
        }

    @property
    def v_prev(self):
        return self._data[V_PREV]

    @v_prev.setter
    def v_prev(self, value):
        self._data.set_value(key=V_PREV, value=value)


    @property
    def v_slow(self):
        return self._data[V_SLOW]

    @v_slow.setter
    def v_slow(self, value):
        self._data.set_value(key=V_SLOW, value=value)

    @property
    def dv_dt_slow(self):
        return self._data[DV_DT_S]

    @dv_dt_slow.setter
    def dv_dt_slow(self, value):
        self._dv_dt_slow = self._data.set_value(key=DV_DT_S, value=value)

    @property
    def tau_low_pass(self):
        return self._data[TAU_LP]

    @tau_low_pass.setter
    def tau_low_pass(self, value):
        self._data.set_value(key=TAU_LP, value=value)
        self.gamma = numpy.exp(-1.0/value)
        self.gamma_complement(1.0 - self.gamma)

    @property
    def gamma(self):
        return self._data[GAMMA]

    @gamma.setter
    def gamma(self, value):
        self._data.set_value(key=GAMMA, value=value)

    @property
    def gamma_complement(self):
        return self._data[GAMMA_COMP]

    @gamma.setter
    def gamma_complement(self, value):
        self._data.set_value(key=GAMMA_COMP, value=value)

    @property
    def v_reset(self):
        return self._data[V_RESET]

    @v_reset.setter
    def v_reset(self, v_reset):
        self._data.set_value(key=V_RESET, value=v_reset)

    @property
    def tau_refrac(self):
        return self._data[TAU_REFRAC]

    @tau_refrac.setter
    def tau_refrac(self, tau_refrac):
        self._data.set_value(key=TAU_REFRAC, value=tau_refrac)

    @property
    def v_max(self):
        return self._data[V_MAX]

    @v_max.setter
    def v_max(self, value):
        self._data.set_value(key=V_MAX, value=value)

    @property
    def v_spike(self):
        return self._data[V_SPIKE]

    @v_spike.setter
    def v_spike(self, value):
        self._data.set_value(key=V_SPIKE, value=value)

    @property
    def v_nmda(self):
        return self._data[V_NMDA]

    @v_nmda.setter
    def v_nmda(self, value):
        self._data.set_value(key=V_NMDA, value=value)

    @overrides(NeuronModelLeakyIntegrate.get_n_neural_parameters)
    def get_n_neural_parameters(self):
        return super(NeuronModelLeakyIntegrateAndFireDvDtNMDA, 
                     self).get_n_neural_parameters() + NUM_EXTRA_PARAMS

    def _tau_refrac_timesteps(self, machine_time_step):
        return self._data[TAU_REFRAC].apply_operation(
            operation=lambda x: numpy.ceil(x / (machine_time_step / 1000.0)))

    @inject_items({"machine_time_step": "MachineTimeStep"})
    def get_neural_parameters(self, machine_time_step):
        params = super(NeuronModelLeakyIntegrateAndFireDvDtNMDA,
                       self).get_neural_parameters()
        params.extend([

            # count down to end of next refractory period [timesteps]
            # int32_t  refract_timer;
            NeuronParameter(
                self._data[COUNTDOWN_TO_REFRACTORY_PERIOD],
                _LIF_DV_TYPES.REFRACT_COUNT.data_type),

            # post-spike reset membrane voltage [mV]
            # REAL     V_reset;
            NeuronParameter(self._data[V_RESET],
                            _LIF_DV_TYPES.V_RESET.data_type),

            # refractory time of neuron [timesteps]
            # int32_t  T_refract;
            NeuronParameter(
                self._tau_refrac_timesteps(machine_time_step),
                _LIF_DV_TYPES.TAU_REFRACT.data_type),

            # Voltage in previous time step
            # REAL     V_prev;
            NeuronParameter(self._data[V_PREV],
                            _LIF_DV_TYPES.V_PREV.data_type),

            # voltage change per time step
            # REAL     dV_dt;
            NeuronParameter(self._data[V_SLOW],
                            _LIF_DV_TYPES.V_SLOW.data_type),

            # low-pass filtered version of voltage change per time step
            # REAL     dV_dt_slow;
            NeuronParameter(self._data[DV_DT_S], 
                            _LIF_DV_TYPES.DV_DT_SLOW.data_type),

            # History weight to filter dV_dt into dV_dt_slow
            # REAL     gamma;
            NeuronParameter(self._data[GAMMA], 
                            _LIF_DV_TYPES.GAMMA.data_type),
            NeuronParameter(self._data[GAMMA_COMP], 
                            _LIF_DV_TYPES.GAMMA_COMP.data_type),

            NeuronParameter(self._data[V_MAX],
                            _LIF_DV_TYPES.V_MAX.data_type),
            NeuronParameter(self._data[V_SPIKE],
                            _LIF_DV_TYPES.V_SPIKE.data_type),
            NeuronParameter(self._data[V_NMDA],
                            _LIF_DV_TYPES.V_NMDA.data_type),

        ])
        return params

    @overrides(NeuronModelLeakyIntegrate.get_neural_parameter_types)
    def get_neural_parameter_types(self):
        if_types = super(NeuronModelLeakyIntegrateAndFireDvDtNMDA,
                         self).get_neural_parameter_types()
        if_types.extend([item.data_type for item in _LIF_DV_TYPES])
        return if_types

    def get_n_cpu_cycles_per_neuron(self):
        # A guess - 20 for the reset procedure
        return super(NeuronModelLeakyIntegrateAndFireDvDtNMDA,
                     self).get_n_cpu_cycles_per_neuron() + \
               _CPU_RESET_CYCLES + \
               _CPU_SPIKE_CYCLES

    @overrides(NeuronModelLeakyIntegrate.get_units)
    def get_units(self, variable):
        if variable in self._my_units:
            return self._my_units[variable]
        return super(NeuronModelLeakyIntegrateAndFireDvDtNMDA,
                     self).get_units(variable)
