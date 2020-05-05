# -*- coding: utf-8 -*-
"""
Module for ScikitTrainer.

A scikit trainer should be used to train a model built with the
scikit-learn API.
"""
from abc import ABC


class ScikitMixin(ABC):
    """
    Scikit Trainer Mixin.

    This class should be included when using a model built
    with the scikit-learn API. It assumes that a model
    instance has a `fit` method.
    """

    # pylint: disable=no-self-use
    def get_model_fit_args(self, dataset):
        """Return arguments to the scikit model fit function."""
        examples, labels = dataset
        return examples, labels

    # pylint: disable=unused-argument
    def fit_model(self, model, step, dataset):
        """Fit the scikit-learn model to the dataset."""
        fit_args = self.get_model_fit_args(dataset)
        model.fit(*fit_args)
