# -*- coding: utf-8 -*-
"""
Module for step trainers.

This module defines a mixin class for all trainers that
use an iterative process for training a model.
"""


class StepTrainerMixin:
    """
    StepTrainer Mixin.

    This class can be used to add a step training behaviour
    to other trainers.
    """

    steps = 0
    epochs = 0
    batch_size = 1

    def __init__(
            self,
            *args,
            steps=None,
            epochs=None,
            batch_size=None,
            **kwargs):

        super().__init__(*args, **kwargs)

        if steps is not None:
            self.steps = steps

        if epochs is not None:
            self.epochs = epochs

        if batch_size is not None:
            self.batch_size = batch_size

    # pylint: disable=no-self-use
    def get_model_prediction(self, model, example):
        """Produce a single prediction from the model."""
        return model(example)

    # pylint: disable=unused-argument
    def train_step(self, model, example, label, step=None):
        """Execute a single training step."""
        prediction = self.get_model_prediction(model, example)
        self.compute_loss(prediction, label)

    def fit_model(self, model, step, dataset):
        """Fit the model to the given dataset."""
        iterator = self.get_dataset_iterator(
            dataset,
            steps=self.steps,
            epochs=self.epochs,
            batch_size=self.batch_size)

        for local_step, (example, label) in enumerate(iterator):
            global_step = local_step + step
            self.train_step(model, example, label, step=global_step)
