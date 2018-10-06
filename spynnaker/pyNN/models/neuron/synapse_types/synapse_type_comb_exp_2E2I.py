from spinn_utilities.overrides import overrides
from spinn_utilities.ranged.abstract_list import AbstractList
from spynnaker.pyNN.models.abstract_models import AbstractContainsUnits
from spinn_utilities.overrides import overrides
from pacman.executor.injection_decorator import inject_items
from .abstract_synapse_type import AbstractSynapseType
from data_specification.enums import DataType
import numpy

EXC_A_RESPONSE = 'exc_a_response'
EXC_CONST_A = 'exc_a_A'
EXC_A_TAU = 'exc_a_tau'
EXC_B_RESPONSE = 'exc_b_response'
EXC_CONST_B = 'exc_b_B'
EXC_B_TAU = 'exc_b_tau'
EXC2_A_RESPONSE = 'exc2_a_response'
EXC2_CONST_A = 'exc2_a_A'
EXC2_A_TAU = 'exc2_a_tau'
EXC2_B_RESPONSE = 'exc2_b_response'
EXC2_CONST_B = 'exc2_b_B'
EXC2_B_TAU = 'exc2_b_tau'
INH_A_RESPONSE = 'inh_a_response'
INH_CONST_A = 'inh_a_A'
INH_A_TAU = 'inh_a_tau'
INH_B_RESPONSE = 'inh_b_response'
INH_CONST_B = 'inh_b_B'
INH_B_TAU = 'inh_b_tau'
INH2_A_RESPONSE = 'inh2_a_response'
INH2_CONST_A = 'inh2_a_A'
INH2_A_TAU = 'inh2_a_tau'
INH2_B_RESPONSE = 'inh2_b_response'
INH2_CONST_B = 'inh2_b_B'
INH2_B_TAU = 'inh2_b_tau'

UNITS = {
    EXC_CONST_A: "(Dimensionless)",
    EXC_A_TAU: "ms",
    EXC_CONST_B: "(Dimensionless)",
    EXC_B_TAU: "ms",
    EXC2_CONST_A: "(Dimensionless)",
    EXC2_A_TAU: "ms",
    EXC2_CONST_B: "(Dimensionless)",
    EXC2_B_TAU: "ms",
    INH_CONST_A: "(Dimensionless)",
    INH_A_TAU: "ms",
    INH_CONST_B: "(Dimensionless)",
    INH_B_TAU: "ms",
    INH2_CONST_A: "(Dimensionless)",
    INH2_A_TAU: "ms",
    INH2_CONST_B: "(Dimensionless)",
    INH2_B_TAU: "ms"
    }

class SynapseTypeCombExp2E2I(AbstractSynapseType):
    slots = [
        '_exc_a_response'
        '_exc_a_A',
        '_exc_a_tau',
        '_exc_B_response'
        '_exc_b_B',
        '_exc_tau_B',
        '_exc2_a_response'
        '_exc2_a_A',
        '_exc2_a_tau',
        '_exc2_B_response'
        '_exc2_b_B',
        '_exc2_tau_B',
        '_inh_a_response'
        '_inh_a_A',
        '_inh_a_tau',
        '_inh_B_response'
        '_inh_b_B',
        '_inh_tau_B',
        '_inh2_a_response'
        '_inh2_a_A',
        '_inh2_a_tau',
        '_inh2_B_response'
        '_inh2_b_B',
        '_inh2_tau_B'
        ]

    def __init__(self,
                exc_a_response,
                exc_a_A,
                exc_a_tau,
                exc_b_response,
                exc_b_B,
                exc_b_tau,

                exc2_a_response,
                exc2_a_A,
                exc2_a_tau,
                exc2_b_response,
                exc2_b_B,
                exc2_b_tau,

                inh_a_response,
                inh_a_A,
                inh_a_tau,
                inh_b_response,
                inh_b_B,
                inh_b_tau,

                inh2_a_response,
                inh2_a_A,
                inh2_a_tau,
                inh2_b_response,
                inh2_b_B,
                inh2_b_tau):

        super(SynapseTypeCombExp2E2I, self).__init__([
            DataType.S1615,  # exc_a_response
            DataType.S1615,  # exc_a
            DataType.U032,   # exc_a_decay
            DataType.U032,   # exc_a_init
            DataType.S1615,  # exc_B_response
            DataType.S1615,  # exc_B
            DataType.U032,   # exc_B_decay
            DataType.U032,   # exc_B_init

            DataType.S1615,  # exc2_a_response
            DataType.S1615,  # exc2_a
            DataType.U032,   # exc2_a_decay
            DataType.U032,   # exc2_a_init
            DataType.S1615,  # exc2_B_response
            DataType.S1615,  # exc2_B
            DataType.U032,   # exc2_B_decay
            DataType.U032,   # exc2_B_init

            DataType.S1615,  # inh_a_response
            DataType.S1615,  # inh_a
            DataType.U032,   # inh_a_decay
            DataType.U032,   # inh_a_init
            DataType.S1615,  # inh_B_response
            DataType.S1615,  # inh_B
            DataType.U032,   # inh_B_decay
            DataType.U032,   # inh_B_init

            DataType.S1615,  # inh2_a_response
            DataType.S1615,  # inh2_a
            DataType.U032,   # inh2_a_decay
            DataType.U032,   # inh2_a_init
            DataType.S1615,  # inh2_B_response
            DataType.S1615,  # inh2_B
            DataType.U032,   # inh2_B_decay
            DataType.U032,   # inh2_B_init
            ])


        # excitatory
        self._exc_a_response = exc_a_response
        self._exc_a_A = exc_a_A
        self._exc_a_tau = exc_a_tau
        self._exc_b_response = exc_b_response
        self._exc_b_B = exc_b_B
        self._exc_b_tau = exc_b_tau

        self.exc_a_A, self.exc_b_B = set_excitatory_scalar(self._exc_a_tau, self._exc_b_tau)

        # excitatory 2
        self._exc2_a_response = exc2_a_response
        self._exc2_a_A = exc2_a_A
        self._exc2_a_tau = exc2_a_tau
        self._exc2_b_response = exc2_b_response
        self._exc2_b_B = exc2_b_B
        self._exc2_b_tau = exc2_b_tau

        self.exc2_a_A, self.exc2_b_B = set_excitatory_scalar(self._exc2_a_tau, self._exc2_b_tau)

        #inhibitory
        self._inh_a_response = inh_a_response
        self._inh_a_A = inh_a_A
        self._inh_a_tau = inh_a_tau
        self._inh_b_response = inh_b_response
        self._inh_b_B = inh_b_B
        self._inh_b_tau = inh_b_tau

        self.inh_a_A, self.inh_b_B = set_excitatory_scalar(self._inh_a_tau, self._inh_b_tau)

        # inhibitory 2
        self._inh2_a_response = inh2_a_response
        self._inh2_a_A = inh2_a_A
        self._inh2_a_tau = inh2_a_tau
        self._inh2_b_response = inh2_b_response
        self._inh2_b_B = inh2_b_B
        self._inh2_b_tau = inh2_b_tau

        self.inh2_a_A, self.inh2_b_B = set_excitatory_scalar(self._inh2_a_tau, self._inh2_b_tau)



    @overrides(AbstractSynapseType.get_n_cpu_cycles)
    def get_n_cpu_cycles(self, n_neurons):
        return 100

    @overrides(AbstractSynapseType.add_parameters)
    def add_parameters(self, parameters):
        parameters[EXC_A_TAU] = self._exc_a_tau
        parameters[EXC_CONST_A] = self._exc_a_A
        parameters[EXC_B_TAU] = self._exc_b_tau
        parameters[EXC_CONST_B] = self._exc_b_B
        parameters[EXC2_A_TAU] = self._exc2_a_tau
        parameters[EXC2_CONST_A] = self._exc2_a_A
        parameters[EXC2_B_TAU] = self._exc2_b_tau
        parameters[EXC2_CONST_B] = self._exc2_b_B
        parameters[INH_A_TAU] = self._inh_a_tau
        parameters[INH_CONST_A] = self._inh_a_A
        parameters[INH_B_TAU] = self._inh_b_tau
        parameters[INH_CONST_B] = self._inh_b_B
        parameters[INH2_A_TAU] = self._inh2_a_tau
        parameters[INH2_CONST_A] = self._inh2_a_A
        parameters[INH2_B_TAU] = self._inh2_b_tau
        parameters[INH2_CONST_B] = self._inh2_b_B

    @overrides(AbstractSynapseType.add_state_variables)
    def add_state_variables(self, state_variables):
        state_variables[EXC_A_RESPONSE] = self._exc_a_response
        state_variables[EXC_B_RESPONSE] = self._exc_b_response
        state_variables[EXC2_A_RESPONSE] = self._exc2_a_response
        state_variables[EXC2_B_RESPONSE] = self._exc2_b_response
        state_variables[INH_A_RESPONSE] = self._inh_a_response
        state_variables[INH_B_RESPONSE] = self._inh_b_response
        state_variables[INH2_A_RESPONSE] = self._inh2_a_response
        state_variables[INH2_B_RESPONSE] = self._inh2_b_response

    @overrides(AbstractSynapseType.get_units)
    def get_units(self, variable):
        return UNITS[variable]

    @overrides(AbstractSynapseType.has_variable)
    def has_variable(self, variable):
        return variable in UNITS

    @inject_items({"ts": "MachineTimeStep"})
    @overrides(AbstractSynapseType.get_values, additional_arguments={'ts'})
    def get_values(self, parameters, state_variables, vertex_slice, ts):

        tsfloat = float(ts) / 1000.0
        decay = lambda x: numpy.exp(-tsfloat / x)  # noqa E731
        init = lambda x: (x / tsfloat) * (1.0 - numpy.exp(-tsfloat / x))  # noqa E731

        # Add the rest of the data
        return [
            # excitatory
            state_variables[EXC_A_RESPONSE],
            parameters[EXC_CONST_A],
            parameters[EXC_A_TAU].apply_operation(decay),
            parameters[EXC_A_TAU].apply_operation(init),
            state_variables[EXC_B_RESPONSE],
            parameters[EXC_CONST_B],
            parameters[EXC_B_TAU].apply_operation(decay),
            parameters[EXC_B_TAU].apply_operation(init),
            # excitatory2
            state_variables[EXC2_A_RESPONSE],
            parameters[EXC2_CONST_A],
            parameters[EXC2_A_TAU].apply_operation(decay),
            parameters[EXC2_A_TAU].apply_operation(init),
            state_variables[EXC2_B_RESPONSE],
            parameters[EXC2_CONST_B],
            parameters[EXC2_B_TAU].apply_operation(decay),
            parameters[EXC2_B_TAU].apply_operation(init),
            # Inhibitory
            state_variables[INH_A_RESPONSE],
            parameters[INH_CONST_A],
            parameters[INH_A_TAU].apply_operation(decay),
            parameters[INH_A_TAU].apply_operation(init),
            state_variables[INH_B_RESPONSE],
            parameters[INH_CONST_B],
            parameters[INH_B_TAU].apply_operation(decay),
            parameters[INH_B_TAU].apply_operation(init),
            # Inhibitory 2
            state_variables[INH2_A_RESPONSE],
            parameters[INH2_CONST_A],
            parameters[INH2_A_TAU].apply_operation(decay),
            parameters[INH2_A_TAU].apply_operation(init),
            state_variables[INH2_B_RESPONSE],
            parameters[INH2_CONST_B],
            parameters[INH2_B_TAU].apply_operation(decay),
            parameters[INH2_B_TAU].apply_operation(init)
            ]

    @overrides(AbstractSynapseType.update_values)
    def update_values(self, values, parameters, state_variables):
        (
            _exc_a_response, _exc_a_A, _exc_a_decay, _exc_a_init,
            _exc_b_response, _exc_b_B, _exc_b_decay, _exc_b_init,

            _exc2_a_response, _exc2_a_A, _exc2_a_decay, _exc2_a_init,
            _exc2_b_response, _exc2_b_B, _exc2_b_decay, _exc2_b_init,

            _inh_a_response, _inh_a_A, _inh_a_decay, _inh_a_init,
            _inh_b_response, _inh_b_B, _inh_b_decay, _inh_b_init,

            _inh2_a_response, _inh2_a_A, _inh2_a_decay, _inh2_a_init,
            _inh2_b_response, _inh2_b_B, _inh2_b_decay, _inh2_b_init,
         ) = values

        state_variables[EXC_A_RESPONSE] = _exc_a_response
        state_variables[EXC_B_RESPONSE] = _exc_b_response
        state_variables[EXC2_A_RESPONSE] = _exc2_a_response
        state_variables[EXC2_B_RESPONSE] = _exc2_b_response
        state_variables[INH_A_RESPONSE] = _inh_a_response
        state_variables[INH_B_RESPONSE] = _inh_b_response
        state_variables[INH2_A_RESPONSE] = _inh2_a_response
        state_variables[INH2_B_RESPONSE] = _inh2_b_response

    @overrides(AbstractSynapseType.get_n_synapse_types)
    def get_n_synapse_types(self):
        return 4

    @overrides(AbstractSynapseType.get_synapse_id_by_target)
    def get_synapse_id_by_target(self, target):
        if target == "excitatory":
            return 0
        elif target == "excitatory2":
            return 1
        elif target == "inhibitory":
            return 2
        elif target == "inhibitory2":
            return 3
        return None

    @overrides(AbstractSynapseType.get_synapse_targets)
    def get_synapse_targets(self):
        return "excitatory", "excitatory2", "inhibitory", "inhibitory2"




    #excitatory
    @property
    def exc_a_response(self):
        return self._exc_a_response

    @exc_a_response.setter
    def exc_a_response(self, exc_a_response):
        self._exc_a_response = exc_a_response

    @property
    def exc_a_A(self):
        return self._exc_a_A

    @exc_a_A.setter
    def exc_a_A(self, exc_a_A):
        self._exc_a_A = exc_a_A

    @property
    def exc_a_tau(self):
        return self._exc_a_tau

    @exc_a_tau.setter
    def exc_a_tau(self, exc_a_tau):
        self._exc_a_tau = exc_a_tau
        self.exc_a_A, self.exc_b_B = set_excitatory_scalar(self._exc_a_tau, self._exc_b_tau)

    @property
    def exc_b_response(self):
        return self._exc_b_response

    @exc_b_response.setter
    def exc_b_response(self, exc_b_response):
        self._exc_b_response = exc_b_response

    @property
    def exc_b_B(self):
        return self._exc_b_B

    @exc_b_B.setter
    def exc_b_B(self, exc_b_B):
        self._exc_b_B = exc_b_B

    @property
    def exc_b_tau(self):
        return self._exc_b_tau

    @exc_b_tau.setter
    def exc_b_tau(self, exc_b_tau):
        self._exc_b_tau = exc_b_tau
        self.exc_a_A, self.exc_b_B = set_excitatory_scalar(self._exc_a_tau, self._exc_b_tau)

    # excitatory2
    @property
    def exc2_a_response(self):
        return self._exc2_a_response

    @exc2_a_response.setter
    def exc2_a_response(self, exc2_a_response):
        self._exc2_a_response = exc2_a_response

    @property
    def exc2_a_A(self):
        return self._exc2_a_A

    @exc2_a_A.setter
    def exc2_a_A(self, exc2_a_A):
        self._exc2_a_A = exc2_a_A

    @property
    def exc2_a_tau(self):
        return self._exc2_a_tau

    @exc2_a_tau.setter
    def exc2_a_tau(self, exc2_a_tau):
        self._exc2_a_tau = exc2_a_tau
        self.exc2_a_A, self.exc2_b_B = set_excitatory_scalar(self._exc2_a_tau, self._exc2_b_tau)

    @property
    def exc2_b_response(self):
        return self._exc2_b_response

    @exc2_b_response.setter
    def exc2_b_response(self, exc2_b_response):
        self._exc2_b_response = exc2_b_response

    @property
    def exc2_b_B(self):
        return self._exc2_b_B

    @exc2_b_B.setter
    def exc2_b_B(self, exc2_b_B):
        self._exc2_b_B = exc2_b_B

    @property
    def exc2_b_tau(self):
        return self._exc2_b_tau

    @exc2_b_tau.setter
    def exc2_b_tau(self, exc2_b_tau):
        self._exc2_b_tau = exc2_b_tau
        self.exc2_a_A, self.exc2_b_B = set_excitatory_scalar(self._exc2_a_tau, self._exc2_b_tau)

    # inhibitory
    @property
    def inh_a_response(self):
        return self._inh_a_response

    @inh_a_response.setter
    def inh_a_response(self, inh_a_response):
        self._inh_a_response = inh_a_response

    @property
    def inh_a_A(self):
        return self._inh_a_A

    @inh_a_A.setter
    def inh_a_A(self, inh_a_A):
        self._inh_a_A = inh_a_A

    @property
    def inh_a_tau(self):
        return self._inh_a_tau

    @inh_a_tau.setter
    def inh_a_tau(self, inh_a_tau):
        self._inh_a_tau = inh_a_tau
        self.inh_a_A, self.inh_b_B = set_excitatory_scalar(self._inh_a_tau, self._inh_b_tau)

    @property
    def inh_b_response(self):
        return self._inh_b_response

    @inh_b_response.setter
    def inh_b_response(self, inh_b_response):
        self._inh_b_response = inh_b_response

    @property
    def inh_b_B(self):
        return self._inh_b_B

    @inh_b_B.setter
    def inh_b_B(self, inh_b_B):
        self._inh_b_B = inh_b_B

    @property
    def inh_b_tau(self):
        return self._inh_b_tau

    @inh_b_tau.setter
    def inh_b_tau(self, inh_b_tau):
        self._inh_b_tau = inh_b_tau
        self.inh_a_A, self.inh_b_B = set_excitatory_scalar(self._inh_a_tau, self._inh_b_tau)

    # inhibitory2
    @property
    def inh2_a_response(self):
        return self._inh2_a_response

    @inh2_a_response.setter
    def inh2_a_response(self, inh2_a_response):
        self._inh2_a_response = inh2_a_response

    @property
    def inh2_a_A(self):
        return self._inh2_a_A

    @inh2_a_A.setter
    def inh2_a_A(self, inh2_a_A):
        self._inh2_a_A = inh2_a_A

    @property
    def inh2_a_tau(self):
        return self._inh2_a_tau

    @inh2_a_tau.setter
    def inh2_a_tau(self, inh2_a_tau):
        self._inh2_a_tau = inh2_a_tau
        self.inh2_a_A, self.inh2_b_B = set_excitatory_scalar(self._inh2_a_tau, self._inh2_b_tau)

    @property
    def inh2_b_response(self):
        return self._inh2_b_response

    @inh2_b_response.setter
    def inh2_b_response(self, inh2_b_response):
        self._inh2_b_response = inh2_b_response

    @property
    def inh2_b_B(self):
        return self._inh2_b_B

    @inh2_b_B.setter
    def inh2_b_B(self, inh2_b_B):
        self._inh2_b_B = inh2_b_B

    @property
    def inh2_b_tau(self):
        return self._inh2_b_tau

    @inh2_b_tau.setter
    def inh2_b_tau(self, inh2_b_tau):
        self._inh2_b_tau = inh2_b_tau
        self.inh2_a_A, self.inh2_b_B = set_excitatory_scalar(self._inh2_a_tau, self._inh2_b_tau)




    ###########################################################

def calc_rise_time(a_tau, b_tau, A=1, B=-1):
    try:
        return numpy.log((A*b_tau) / (-B*a_tau)) * ( (a_tau*b_tau) / (b_tau - a_tau) )
    except:
        "calculation failed: ensure A!=B and that they are of opposite sign"

def calc_scalar_f(a_tau, b_tau):
    t_rise = calc_rise_time(a_tau = a_tau, b_tau=b_tau)
    return 1/(numpy.exp(-t_rise/a_tau) - numpy.exp(-t_rise/b_tau))

def set_excitatory_scalar(exc_a_tau, exc_b_tau):
    sf = calc_scalar_f(a_tau = exc_a_tau, b_tau=exc_b_tau)
    a_A = sf
    b_B = -sf
    return a_A, b_B
