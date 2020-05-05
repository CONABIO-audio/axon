# -*- coding: utf-8 -*-
"""
TF Trainer module.

This module defines classes that aids the construction of trainers
meant to be used on models defined with the tensorflow API.
"""
from abc import ABC


class TFTrainerMixin(ABC):  # pylint: disable=abstract-method
    """
    Tensorflow trainer base class.

    All tensorflow training processes must inherit from this class.
    """

    def __init__(
            self,
            *args,
            steps=None,
            epochs=None,
            batch_size=None,
            **kwargs):
        super().__init__(*args, **kwargs)

        if steps and epochs:
            message = 'Steps and epochs cannot be set simultaneously'
            raise ValueError(message)

        self.batch_size = batch_size
        self.steps = steps
        self.epochs = epochs

    # pylint: disable=no-self-use
    def get_dataset_iterator(
            self,
            dataset,
            steps=None,
            epochs=None,
            batch_size=None):
        """Build the data iterator used to feed the training process."""
        if steps:
            return dataset.iter(steps=steps, batch_size=batch_size)
        return dataset.iter(epochs=epochs, batch_size=batch_size)

    def fit_model(self, model, step, dataset, steps=None, epochs=None):
        """Fit the model to the given dataset."""
        iterator = self.get_dataset_iterator(
            dataset,
            steps=steps,
            epochs=epochs,
            batch_size=self.batch_size)

        for local_step, (example, label) in enumerate(iterator):
            global_step = local_step + step
            self.train_step(model, example, label, step=global_step)

    # pylint: disable=unused-argument
    def train_step(self, model, example, label, step=None):
        """Execute a single training step."""
        prediction = self.get_model_prediction(model, example)
        metrics, gradients = self.update_model(prediction, label)
        self.log_metrics({
            f'{key}': value
            for key, value in metrics.items()
        })
        print(gradients)

    # pylint: disable=no-self-use
    def get_model_prediction(self, model, example):
        """Run the model on a single example."""
        return model(example)

    def should_stop(self, *args, **kwargs) -> bool:
        """Evaluate stopping criteria."""

    def train(self, step=None, steps=None, epochs=None):
        """Train model during the specified number of steps or epochs."""
        if step is None:
            step = self.step

        if steps is None:
            steps = self.steps

        if epochs is None:
            epochs = self.epochs

        if steps and epochs:
            message = 'Steps and epochs cannot be set simultaneously.'
            raise ValueError(message)

        if not steps and not epochs:
            message = 'Steps or epochs must be set.'
            raise ValueError(message)

        model, step, dataset = self.initialize_training(step=step)
        self.fit_model(model, step, dataset, steps=steps, epochs=epochs)
