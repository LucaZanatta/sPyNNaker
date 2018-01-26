# main interface to use the spynnaker related tools.
from spynnaker.pyNN.models.neuron.abstract_population_vertex \
    import AbstractPopulationVertex

from spynnaker.pyNN.models.neuron.input_types.input_type_current \
    import InputTypeCurrent
from spynnaker.pyNN.models.neuron.neuron_models \
    import NeuronModelLeakyIntegrateAndFire
from spynnaker.pyNN.models.neuron.synapse_types.synapse_type_exp_supervision \
    import ExpSupervision
from spynnaker.pyNN.models.neuron.threshold_types.threshold_type_adaptive \
    import ThresholdTypeAdaptive
# global objects
DEFAULT_MAX_ATOMS_PER_CORE = 255

class IFCurrExpSupervisionAdaptive(AbstractPopulationVertex):

    # the maximum number of atoms per core that can be supported
    _model_based_max_atoms_per_core = DEFAULT_MAX_ATOMS_PER_CORE

    # default parameters for this build. Used when end user has not entered any
    default_parameters = {
        'tau_m': 20.0, 'cm': 1.0, 'v_rest': -65.0, 'v_reset': -65.0,
        'v_thresh': -50.0,
        'min_thresh': -60.0, 'max_thresh': -30.0,
        'up_thresh': 1., 'down_thresh': 0.005,
        'tau_syn_E': 5.0, 'tau_syn_I': 5.0,
        'tau_refrac': 0.1, 'i_offset': 0
    }

    def __init__(
            self, n_neurons,
            spikes_per_second=None, ring_buffer_sigma=None,
            incoming_spike_buffer_size=None,
            constraints=None, label=None,
            tau_m=default_parameters['tau_m'],
            cm=default_parameters['cm'],
            v_rest=default_parameters['v_rest'],
            v_reset=default_parameters['v_reset'],
            v_thresh=default_parameters['v_thresh'],
            min_thresh=default_parameters['min_thresh'],
            max_thresh=default_parameters['max_thresh'],
            up_thresh=default_parameters['up_thresh'],
            down_thresh=default_parameters['down_thresh'],
            tau_syn_E=default_parameters['tau_syn_E'],
            tau_syn_I=default_parameters['tau_syn_I'],
            tau_refrac=default_parameters['tau_refrac'],
            i_offset=default_parameters['i_offset'],
            v_init=None):

            neuron_model = NeuronModelLeakyIntegrateAndFire(
                n_neurons, v_init, v_rest, tau_m, cm, i_offset,
                v_reset, tau_refrac)
            synapse_type = ExpSupervision(
                n_neurons, tau_syn_E, tau_syn_I)
            input_type = InputTypeCurrent()
            threshold_type = ThresholdTypeAdaptive(n_neurons, v_thresh,
                                min_thresh, max_thresh, up_thresh, down_thresh)

            # create additional inputs
            additional_input = None

            # instantiate the sPyNNaker system by initialising
            #  the AbstractPopulationVertex
            AbstractPopulationVertex.__init__(

                # standard inputs, do not need to change.
                self, n_neurons=n_neurons, label=label,
                spikes_per_second=spikes_per_second,
                ring_buffer_sigma=ring_buffer_sigma,
                incoming_spike_buffer_size=incoming_spike_buffer_size,

                max_atoms_per_core=(
                    IFCurrExpSupervisionAdaptive._model_based_max_atoms_per_core),

                # the various model types
                neuron_model=neuron_model, input_type=input_type,
                synapse_type=synapse_type, threshold_type=threshold_type,
                additional_input=additional_input,

                # the model a name (shown in reports)
                model_name="IF_curr_exp_supervision_adpt",

                # the matching binary name
                binary="IF_curr_exp_supervision_adpt.aplx")

    @staticmethod
    def set_model_max_atoms_per_core(new_value=DEFAULT_MAX_ATOMS_PER_CORE):

        IFCurrExpSupervisionAdaptive._model_based_max_atoms_per_core = new_value

    @staticmethod
    def get_max_atoms_per_core():
        return IFCurrExpSupervisionAdaptive._model_based_max_atoms_per_core
