from spynnaker.pyNN.models.neuron.neuron_models import NeuronModelIzhDvDt
from spynnaker.pyNN.models.neuron.synapse_types import SynapseTypeExponential
from spynnaker.pyNN.models.neuron.input_types import InputTypeCurrent
from spynnaker.pyNN.models.neuron.threshold_types import ThresholdTypeAdaptive
from spynnaker.pyNN.models.neuron import AbstractPopulationVertex

# global objects
DEFAULT_MAX_ATOMS_PER_CORE = 255
_IZK_THRESHOLD = 30.0
_apv_defs = AbstractPopulationVertex.non_pynn_default_parameters


class IzkCurrExpDvDtAdaptive(AbstractPopulationVertex):

    _model_based_max_atoms_per_core = DEFAULT_MAX_ATOMS_PER_CORE

    default_parameters = {
        'a': 0.02, 'c': -65.0, 'b': 0.2, 'd': 2.0, 'i_offset': 0,
        'tau_syn_E': 5.0, 'tau_syn_I': 5.0, 'isyn_exc': 0, 'isyn_inh': 0,
        'tau_low_pass': 20.,
        'min_thresh': 25.0, 'max_thresh': 30.0,
        'up_thresh': 0.1, 'down_thresh': 0.01,
}

    initialize_parameters = {'u_init': -14.0, 'v_init': -70.0}

    # noinspection PyPep8Naming
    def __init__(
            self, n_neurons,
            spikes_per_second=_apv_defs['spikes_per_second'],
            ring_buffer_sigma=_apv_defs['ring_buffer_sigma'],
            incoming_spike_buffer_size=_apv_defs['incoming_spike_buffer_size'],
            constraints=_apv_defs['constraints'],
            label=_apv_defs['label'],
            a=default_parameters['a'], b=default_parameters['b'],
            c=default_parameters['c'], d=default_parameters['d'],
            i_offset=default_parameters['i_offset'],
            u_init=initialize_parameters['u_init'],
            v_init=initialize_parameters['v_init'],
            tau_syn_E=default_parameters['tau_syn_E'],
            tau_syn_I=default_parameters['tau_syn_I'],
            isyn_exc=default_parameters['isyn_exc'],
            isyn_inh=default_parameters['isyn_inh'],
            tau_low_pass=default_parameters['tau_low_pass'],
            min_thresh=default_parameters['min_thresh'],
            max_thresh=default_parameters['max_thresh'],
            up_thresh=default_parameters['up_thresh'],
            down_thresh=default_parameters['down_thresh'],):
        # pylint: disable=too-many-arguments, too-many-locals
        neuron_model = NeuronModelIzhDvDt(
            n_neurons, a, b, c, d, v_init, u_init, i_offset)
        synapse_type = SynapseTypeExponential(
            n_neurons, tau_syn_E, tau_syn_I, isyn_exc, isyn_inh)
        input_type = InputTypeCurrent()
        threshold_type = ThresholdTypeAdaptive(n_neurons, min_thresh,
                            min_thresh, max_thresh, up_thresh, down_thresh)

        super(IzkCurrExpDvDtAdaptive, self).__init__(
            n_neurons=n_neurons, binary="IZK_curr_exp_dv.aplx", label=label,
            max_atoms_per_core=IzkCurrExpDvDt._model_based_max_atoms_per_core,
            spikes_per_second=spikes_per_second,
            ring_buffer_sigma=ring_buffer_sigma,
            incoming_spike_buffer_size=incoming_spike_buffer_size,
            model_name="IZK_curr_exp_dv", neuron_model=neuron_model,
            input_type=input_type, synapse_type=synapse_type,
            threshold_type=threshold_type, constraints=constraints)

    @staticmethod
    def set_model_max_atoms_per_core(new_value=DEFAULT_MAX_ATOMS_PER_CORE):
        IzkCurrExpDvDtAdaptive._model_based_max_atoms_per_core = new_value

    @staticmethod
    def get_max_atoms_per_core():
        return IzkCurrExpDvDtAdaptive._model_based_max_atoms_per_core
