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
        """Load persisted model.

        Load model with parameters from checkpoint file.
        """

    @abstractmethod
    def save(self, path):
        """Persist model.

        Persist model with current parameters to path.
        """

    def __call__(self, data):
        """Run action and return output.

        For the sake of consistency and proper record, this method should not
        be modified. If the behaviour of model execution is to be changed,
        'build_architecture', 'build_preprocessor' or 'build_action' should be
        overwritten instead.
        """
        return self.action(data)


import tensorflow as tf


class TFModel(Model, ABC):
    graph = None
    mode = 'predict'
    batch_size = 1

    def __init__(self, *args, graph, batch_size=None, **kwargs):
        if graph is not None:
            self.graph = graph
        else:
            self.graph = tf.Graph()
        if batch_size is not None:
            if batch_size <= 0:
                raise ValueError("Batch size should be greater than 0.")
            self.batch_size = batch_size

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
