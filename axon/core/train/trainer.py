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
    dataset = None
    model = None
    checkpoint_dir = ""
    step = 0

    def __init__(
            self,
            *args,
            step=None,

            **kwargs):
        super().__init__(*args, **kwargs)

        if steps is not None:
            self.steps = steps

    def build_model(self):
        model = self.model(batch_size=self.batch_size)
        return model

    def build_dataset(self):
        return self.dataset()

    def load_checkpoint(self, model, step):
        """Read checkpoint parameters and load."""
        ckp_path = os.path.join(self.checkpoint_dir, f'{step}.ckp')
        if self.wdir is not None:
            ckp_path = os.path.join(self.wdir, ckp_path)
        self._step = model.load(ckp_path)

    def save_checkpoint(self, step):
        """Write checkpoint to checkpoint directory."""

    def initialize_training(self, step=None):
        model = self.build_model()
        step = self.load_checkpoint(model, step)
        dataset = self.build_dataset()
        return model, step, dataset

    def get_model_fit_args(self, dataset):
        examples, labels = dataset
        return examples, labels

    def fit_model(self, model, step, dataset):
        fit_args = self.get_model_fit_args(dataset)
        model.fit(*fit_args)

    def train_step(self, model, example, label, step=None):
        prediction = self.get_model_prediction(model, example)
        loss = self.compute_loss(prediction, label)

    def get_model_prediction(self, model, example):
        return model(example)

    def train(self, step=None):
        """Train model during the specified number of steps or epochs."""
        if step is None:
            step = self.step

        model, step, dataset = self.initialize_train(step=step)
        self.fit_model(model, step, dataset, steps=steps, epochs=epochs)

    def run(self):
        self.train()


class TFTrainer(Trainer, ABC):  # pylint: disable=abstract-method
    """
    Tensorflow trainer base class.

    All tensorflow training processes must inherit from this class.
    """

    def __init__(self, *args, steps=None, epochs=None, **kwargs):
        super().__init__(*args, **kwargs)

        if steps and epochs:
            message = 'Steps and epochs cannot be set simultaneously'
            raise ValueError(message)

        if step is not None:
            self.step = step

        if epochs is not None:
            self.epochs = epochs

    def get_dataset_iterator(self, dataset, steps=None, epochs=None, batch_size=None):
        if steps:
            return dataset.iter(steps=steps, batch_size=batch_size)
        return dataset.iter(epochs=epochs, batch_size=batch_size)

    def fit_model(self, model, step, dataset, steps=None, epochs=None):
        iterator = self.get_dataset_iterator(
            dataset,
            steps=steps,
            epochs=epochs,
            batch_size=self.batch_size)

        for local_step, (example, label) in enumerate(iterator):
            global_step = local_step + step
            self.train_step(model, example, label, step=global_step)

    def train_step(self, model, example, label, step=None):
        prediction = self.get_model_prediction(model, example)
        metrics, gradients = self.update_model(prediction, label)
        self.log_metrics({
            f'{key}': value
            for key, value in metrics.items()
        })

    def get_model_prediction(self, model, example):
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

        model, step, dataset = self.initialize_train(step=step)
        self.fit_model(model, step, dataset, steps=steps, epochs=epochs)
