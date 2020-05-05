# -*- coding: utf-8 -*-
"""
Evaluator module.

This module defines the base class for all evaluation processes.
"""

from abc import ABC
from abc import abstractmethod
import os
import pandas as pd
from axon.core.processes.mlflow_process import MLFlowProcess


class Metric(ABC):
    """Abstract class for all evaluation metrics."""

    @abstractmethod
    @property
    def name(self):
        """Return metric's name."""

    @abstractmethod
    def apply(self, prediction, target):
        """Apply metric with input prediction and ground truth"""

    def __call__(self, prediction, target):
        return self.apply(prediction, target)


class Evaluator(MLFlowProcess, ABC):  # pylint: disable=abstract-method
    """Abstract class for all evaluators."""

    evaluations = []
    output_dir = ""
    output_name = "evaluation.csv"

    def __init__(self,
                 *args,
                 model,
                 dataset,
                 evaluations=None,
                 output_dir=None,
                 output_name=None,
                 **kwargs):
        if evaluations is not None:
            if not isinstance(evaluations, (tuple, list)):
                raise ValueError("Argument 'evaluations' must be a list of "
                                 "objects of class Metric.")
            for obj in evaluations:
                if not isinstance(obj, Metric):
                    raise ValueError("All evaluations must be of type Metric.")
            self.evaluations = evaluations
        if output_dir is not None:
            if not isinstance(output_dir, str):
                raise ValueError("Argument 'output_dir' must be a string.")
            self.output_dir = output_dir

        if output_name is not None:
            if not isinstance(output_name, str):
                raise ValueError("Argument 'output_name' must be a string.")
            self.output_name = output_name

        self.model = model
        self.dataset = dataset

        super().__init__(*args, **kwargs)

        self.outs['output_dir'] = self.output_dir

    def evaluate_single(self, prediction, target):
        """Evaluate a single example."""
        results = []
        for metric in self.evaluations:
            result = metric(prediction, target)
            results.append(result)

        return results

    def get_example_iterator(self, dataset):
        """Return example iterator."""
        for id, example, target in dataset:
            yield id, example, target

    def parse_metrics_results(self, results):
        """Parse results."""
        parsed = {}

        for result in results:
            parsed.update(result)

        return parsed

    def parse_targets(self, target):
        """Parse target to correct format."""
        return target

    def parse_examples(self, example):
        """Parse example to correct format."""
        return example

    def parse_predictions(self, prediction):
        """Parse prediction to correct format."""
        return prediction

    def build_model(self):
        """Build the model to evaluate.

        Abstract method. Any trainer should implement this
        functionality.
        """
        return self.model()

    def build_dataset(self):
        """Build the evaluating dataset.

        Abstract method. Any trainer should implement this
        functionality.
        """
        return self.dataset()

    def get_prediction(self, model, example):
        """Run model with example."""
        return model(example)

    def evaluate(self):
        """Evaluate model with dataset."""
        model = self.build_model()
        dataset = self.build_dataset()

        results = []
        example_iterator = self.get_example_iterator(dataset)
        for example_id, example, target in example_iterator:
            prediction = self.get_prediction(model, example)
            evaluation_result = self.evaluate_single(prediction, target)

            # Get metric results info
            parsed_results = self.parse_metrics_results(evaluation_result)

            # Get additional metadata
            parsed_example_metadata = self.parse_examples(example)
            parsed_prediction_metadata = self.parse_predictions(prediction)
            parsed_target_metadata = self.parse_targets(target)

            data = {
                'id': example_id,
                **parsed_example_metadata,
                **parsed_target_metadata,
                **parsed_prediction_metadata,
                **parsed_results
            }
            results.append(data)

        results = pd.DataFrame(results)
        self.log_results(results)
        self.save_results(results)

    def get_metric_columns(self):
        """Get metric names in order."""
        columns = []
        for metric in self.evaluations:
            columns.append(metric.name)
        return columns

    def log_results(self, results):
        """Log evaluation results."""
        metric_columns = self.get_metric_columns()
        subset = results[metric_columns]

        means = subset.mean().to_dict()
        self.log_metrics({
            f'{key}_mean': value
            for key, value in means.items()
        })

        stds = subset.std().to_dict()
        self.log_metrics({
            f'{key}_std': value
            for key, value in stds.items()
        })

    def get_result_path(self):
        """Get path for result file saving."""
        relative_path = os.path.join(self.output_dir, self.output_name)

        if self.wdir is not None:
            return os.path.join(self.wdir, relative_path)

        return relative_path

    def save_results(self, results):
        """Save dataframe to CSV file."""
        results.to_csv(path=self.get_result_path())

    def run(self):
        """Run evaluator."""
        self.evaluate()
