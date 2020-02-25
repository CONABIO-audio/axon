# -*- coding: utf-8 -*-
"""Trainer Module.

This module defines the base class for all training processes.
"""
from abc import ABC
from abc import abstractmethod
from axon.processes import Process


class Trainer(Process, ABC):
    """Trainer base class.

    A trainer is a kind of process that takes a model and a dataset and outputs
    a fitted model with training statistics.
    """

    target_class = None
    checkpoint_each = 10
    stop_thresh = None
    write_dir = ""
    pipeline = None

    @abstractmethod
    def build_pipeline(self):
        """Training pipeline.

        This method should construct the whole training pipeline to be run
        using method 'start'.
        """

    @abstractmethod
    def train(self, model=None):
        """Training method.

        This method should train the current target for one step.
        """

    @abstractmethod
    def write_checkpoint(self):
        """Checkpoint writer.

        This method should write checkpoints with all the needed information
        in order to continue the training process from current step.
        """

    @abstractmethod
    def load_checkpoint(self, step_number):
        """Checkpoint loader.

        This method should read the specified persisted checkpoint and load
        parameters.
        """

    @abstractmethod
    def checkpoint_exists(self, step_number):
        """Checkpoint existence.

        This method should check if checkpoint exists.
        """

    @abstractmethod
    def start(self):
        """Start training pipeline.

        This method should start the training pipeline.
        """

    @abstractmethod
    def stop(self):
        """Stop training pipeline.

        This method should determine how to stop training in a healthy
        way.
        """

    @abstractmethod
    def summary(self, start_step=None, stop_step=None):
        """Training summary.

        This method should output basic statistics about the training
        process between the specified training steps.
        """
