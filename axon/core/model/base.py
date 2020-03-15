"""Base classes for all models."""
from abc import ABC
from abc import abstractmethod


class Model(ABC):
    _action = None
    _architecture = None
    preprocessor = None

    @property
    def action(self):
        """Return model's action."""
        if self._action is None:
            self._action = self.build_action()
        return self._action

    @property
    def architecture(self):
        """Return model's architecture."""
        if self._architecture is None:
            self._architecture = self.build_architecture()
        return self._architecture

    @abstractmethod
    def preprocess(self, data):
        """Preprocess input data."""
        if self.preprocessor is not None:
            return self.preprocessor(data)
        return data

    @abstractmethod
    def build_preprocessor(self):
        """Build preprocess pipeline and return callable object.

        This method builds the pre-processing pipeline or imports an object
        of class Preprocess and returns it.
        """

    @abstractmethod
    def build_architecture(self):
        """Build model architecture.

        This method returns the full model architecture to be instantiated.
        """

    @abstractmethod
    def build_action(self):
        """Build model action.

        This method returns model mapping given by architecture and
        preprocessing as a callable object that returns model predictions.
        """

    @abstractmethod
    def load(self, path):
        """Load saved params.

        Load model parameters from checkpoint file.
        """

    def __call__(self, data):
        """Run action and return output.

        For consistency and proper record, this method should not be
        overwritten. If the behaviour of model execution is to be changed,
        'build_architecture', 'build_preprocessor' or 'build_action' should be
        overwritten instead.
        """
        return self.action(data)
