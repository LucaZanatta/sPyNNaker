from six import add_metaclass
from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty


@add_metaclass(ABCMeta)
class AbstractWeightDependence(object):

    def __init__(self):
        self._a_plus = None
        self._a_minus = None

    def set_a_plus_a_minus(self, a_plus, a_minus):
        self._a_plus = a_plus
        self._a_minus = a_minus

    @property
    def A_plus(self):
        return self._A_plus

    @A_plus.setter
    def A_plus(self, new_value):
        self._a_plus = new_value

    @property
    def A_minus(self):
        return self._A_minus

    @A_minus.setter
    def A_minus(self, new_value):
        self._a_minus = new_value

    def get_provenance_data(self, pre_population_label, post_population_label):
        """ Get any provenance data
        """
        return list()

    @abstractmethod
    def is_same_as(self, weight_dependence):
        """ Determine if this weight dependence is the same as another
        """

    @abstractproperty
    def vertex_executable_suffix(self):
        """ The suffix to be appended to the vertex executable for this rule
        """

    @abstractmethod
    def get_parameters_sdram_usage_in_bytes(
            self, n_synapse_types, n_weight_terms):
        """ Get the amount of SDRAM used by the parameters of this rule
        """

    @abstractmethod
    def write_parameters(
            self, spec, machine_time_step, weight_scales, n_weight_terms):
        """ Write the parameters of the rule to the spec
        """

    @abstractproperty
    def weight_maximum(self):
        """ The maximum weight that will ever be set in a synapse as a result\
            of this rule
        """
