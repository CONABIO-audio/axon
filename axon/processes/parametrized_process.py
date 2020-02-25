"""Parametrized process module.

This module defines the base class for all parametrized process.
This are process that are defined by an architecture, or a parametrized family
of processes, and a definite selection of parameters.
"""
from axon.processes.base import Process


class ParametrizedProcess(Process):
    """Parametrized process base class.

    A parametrized process is a process that has a particular architecture
    from which to build an action based on parameters. The specified
    architecture should have compatible input, output and parameters datatypes.
    """

    architecture = None
    current_params = None

    def __init__(self, params, architecture=None, **kwargs):
        if architecture is not None:
            self.architecture = architecture

        if not self.validate_architecture():
            raise ValueError("Architecture and datatypes not compatible.")

        self.set_params(params)
        super().__init__(**kwargs)

    def validate_architecture(self):
        """Verify architecture compatibility."""
        if self.architecture is None:
            return False

        return (
            self.architecture.input_dtype == self.input_dtype and
            self.architecture.output_dtype == self.output_dtype)

    def set_params(self, params):
        """Validate params and build internal action."""
        if not self.architecture.validate_params(params):
            raise ValueError("Architecture not compatible with process specs.")

        self.current_params = params
        self.action = self.architecture.build_action(self.current_params)

    def get_params(self):
        """Return current parameters."""
        return self.current_params

    def get_action(self):
        """Return process action."""
        return self.action

    def run(self, *args, **kwargs):
        """Run action."""
        return self.action(*args, **kwargs)
