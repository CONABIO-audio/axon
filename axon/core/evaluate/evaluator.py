# -*- coding: utf-8 -*-
"""
Evaluator module.

This module defines the base class for all evaluation processes.
"""
from abc import ABC
import os
import pandas as pd
from axon.core.processes.mlflow_process import MLFlowProcess


class Evaluator(MLFlowProcess, ABC):  # pylint: disable=abstract-method
    """Evaluator class."""

    metrics = None
    dataset = None
    model = None
    output_dir = ""
    output_name = "evaluation.csv"

    def evaluate_single(self, prediction, target):
        """Evaluate a single example."""
        results = []
        for metric in self.metrics:
            result = metric(prediction, target)
            results.append(result)

        return results

    def get_example_iterator(self, dataset):
        for id, example, target in dataset:
            yield id, example, target

    def summary(self):
        """Read or generate evaluation and generate descriptive statistics."""

    def parse_metrics_results(self, results):
        parsed = {}

        for result in results:
            parsed.update(result)

        return parsed

    def parse_targets(self, target):
        return target

    def parse_examples(self, example):
        return {}

    def parse_predictions(self, prediction):
        return {}

    def build_model(self):
        return self.model()

    def build_dataset(self):
        return self.dataset()

    def get_prediction(self, model, example):
        return model(example)

    def evaluate(self):
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
        columns = []
        for metric in self.metrics:
            columns.append(metric.names)
        return columns

    def log_results(self, results):
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
        self.evaluate()


class BatchEvaluator(Evaluator):
    batch_size = 10

    def __init__(self, *args, batch_size=None, **kwargs):
        super().__init__(*args, **kwargs)

        if batch_size is not None:
            self.batch_size = batch_size

    def get_example_iterator(self, dataset):
        for id, example, target in dataset.batch(self.batch_size):
            yield id, example, target

    def evaluate(self):
        model = self.build_model(batch_size=self.batch_size)
        dataset = self.build_dataset()

        results = []
        example_iterator = self.get_example_iterator(dataset)
        for example_id_batch, example_batch, target_batch in example_iterator:
            prediction_batch = self.get_prediction(model, example_batch)

            subiterator = zip(
                example_id_batch,
                example_batch,
                target_batch,
                prediction_batch)
            for example_id, example, target, prediction in subiterator:
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
