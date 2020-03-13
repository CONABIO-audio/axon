# -*- coding: utf-8 -*-
"""
Trainer module.

In this module the base class for al Trainer processes is defined.
"""
from abc import ABC
import os
from axon.core.processes.mlflow_process import MLFlowProcess


class Trainer(MLFlowProcess, ABC):  # pylint: disable=abstract-method
    """
    Trainer base class.

    All training processes must inherit from this class.
    """
    metrics = None
    model = None
    checkpoint_dir = ""
    batch_size = 1
    optimizer = None
    loss = None
    _step = 0

    def build_model(self):
        return self.model(batch_size=self.batch_size)

    def load_checkpoint(self, step):
        """Read checkpoint parameters and load."""
        ckp_path = os.path.join(self.checkpoint_dir, f'{step}.ckp')
        if self.wdir is not None:
            ckp_path = os.path.join(self.wdir, ckp_path)
        self._step = self.model.load(ckp_path)

    def save_checkpoint(self, step):
        """Write checkpoint to checkpoint directory."""

    def stop(self, force):
        """Evaluate stopping criteria and stop if any is true."""

    def train(self, steps=None, epochs=None):
        """Train model during the specified number of steps or epochs."""
