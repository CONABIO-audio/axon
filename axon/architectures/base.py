"""Architecture Module.

This module defines the base class for all Architectures.
"""
from abc import ABC
from abc import abstractmethod

from axon.datatypes import DataType
from axon.processes.parametrized_process import ParametrizedProcess


class ArchitectureBase(ABC):
    """Architecture base class.

    An architecture is an abstract class that specifies the internal structure
    of a mapping between data.
    """

    name = None
    input_dtype = None
    output_dtype = None
    params_class = None
    
    def __init__(self):
        assert isinstance(self.output_dtype, DataType)
        assert isinstance(self.input_dtype, DataType)
        # assert isinstance(self.get_params_class(), Parameters)


    @abstractmethod
    def build_action(self, params):
        """Build process action.

        This method should build all computation steps and return a callable
        function with compatible input and output types.
        """


    @abstractmethod
    def validate_params(self, params):
        """Validate input parameters."""

    def get_params_class(self):
        if getattr(self, 'params_class', None) is not None:
            return self.params_class

        raise NotImplementedError('No parameter class was provided')

    def set_params(self, params):
        class InstantiatedProcess(ParametrizedProcess):
            architecture = self
            current_params = params

            def get_partial_output(self, name):
                pass

        return InstantiatedProcess
