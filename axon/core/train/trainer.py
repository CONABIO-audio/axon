# -*- coding: utf-8 -*-
"""
Trainer module.

In this module the base class for al Trainer processes is defined.
"""
from abc import ABC
from abc import abstractmethod
import os
from axon.core.processes.mlflow_process import MLFlowProcess


class Trainer(MLFlowProcess, ABC):  # pylint: disable=abstract-method
    """
    Trainer base class.

    All training processes must inherit from this class.
    """

    checkpoint_dir = ""
    checkpoint_name = "checkpoint.ckpt"
    step = 0

    def __init__(
            self,
            *args,
            step=None,
            checkpoint_dir=None,
            checkpoint_name=None,
            **kwargs):

        if checkpoint_dir is not None:
            self.checkpoint_dir = checkpoint_dir

        if checkpoint_name is not None:
            self.checkpoint_name = checkpoint_name

        if step is not None:
            self.step = step

        super().__init__(*args, **kwargs)

        self.outs['checkpoint_dir'] = self.checkpoint_dir

    @abstractmethod
    def build_model(self):
        """Build the model to train.

        Abstract method. Any trainer should implement this
        functionality.
        """

    @abstractmethod
    def build_dataset(self):
        """Build the training dataset.

        Abstract method. Any trainer should implement this
        functionality.
        """

    def get_checkpoint_path(self, step=None):
        """Get path to the desired model checkpoint."""
        if step is None:
            return os.path.join(
                self.checkpoint_dir,
                self.checkpoint_name)
        return os.path.join(self.checkpoint_dir, f'{step}.ckpt')

    def load_checkpoint(self, model, step=None):
        """Read checkpoint parameters and load."""
        checkpoint_path = self.get_checkpoint_path(step=step)
        if self.wdir is not None:
            checkpoint_path = os.path.join(self.wdir, checkpoint_path)
        return model.load(checkpoint_path)

    def save_checkpoint(self, step):
        """Write checkpoint to checkpoint directory."""

    def initialize_training(self, step=None):
        """Build training model and dataset."""
        model = self.build_model()
        dataset = self.build_dataset()
        step = self.load_checkpoint(model, step=step)
        return model, step, dataset

    @abstractmethod
    def fit_model(self, model, step, dataset):
        """Fit the model to the given data.

        Abstract method. Any trainer should implement this
        functionality.
        """

    def train(self, step=None):
        """Train model during the specified number of steps or epochs."""
        if step is None:
            step = self.step

        model, step, dataset = self.initialize_training(step=step)
        self.fit_model(model, step, dataset)

    def run(self, *args, **kwargs):
        """Run the training process."""
        self.train()
