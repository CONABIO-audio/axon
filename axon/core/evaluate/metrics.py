"""A collection of useful evaluation metrics."""
from .base import Metric
import numpy as np


class EuclideanDistance(Metric):

    @property
    def name(self):
        return "euclidean_distance"

    def apply(self, prediction, target):
        return np.linalg.norm(target - prediction)


class FalsePositives(Metric):

    @property
    def name(self):
        return "false_positives"

    def apply(self, prediction, target):
        diff = prediction - target
        return np.sum(diff[diff == 1])
