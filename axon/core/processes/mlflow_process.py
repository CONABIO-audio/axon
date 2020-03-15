# -*- coding: utf-8 -*-
"""
MLFlow Process Module.

This modules contains the base definition of a process that utilizes mlflow to
log run information, and associated mlflow utilities.
"""
import mlflow
from axon.core.processes.base import Process


class MLFlowMixin:
    """MLFlow Mixin for processes.

    This mixin will provides functionally to record all
    of the process runs using mlflow.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.experiment = kwargs.get('experiment', None)
        self.run_name = kwargs.get('run_name', None)
        self.run_id = kwargs.get('run_id', None)
        self.experiment_id = kwargs.get('experiment_id', None)
        self.nested = kwargs.get('nested', None)

        self.mlflow_run = None

        if 'tracking_uri' in kwargs:
            mlflow.set_tracking_uri(kwargs['tracking_uri'])

    def start_run(self):
        """Start an mlflow run.

        Uses the configurations passed at intialization.
        """
        return mlflow.start_run(
            run_id=self.run_id,
            experiment_id=self.experiment_id,
            run_name=self.run_name,
            nested=self.nested)

    @staticmethod
    def log_param(key, value):
        """Log parameter using mlflow logging utilities."""
        mlflow.log_param(key, value)

    @staticmethod
    def log_params(params):
        """Log parameters using mlflow logging utilities."""
        mlflow.log_params(params)

    @staticmethod
    def log_metric(key, value, step=None):
        """Log a metric using mlflow logging utilities."""
        mlflow.log_metric(key, value, step=step)

    @staticmethod
    def log_metrics(metrics, step=None):
        """Log metrics using mlflow logging utilities."""
        mlflow.log_metrics(metrics, step=step)

    def __call__(self, *args, **kwargs):
        """Run the process.

        This method uses the user defined method 'run' to compute
        the output for the given inputs. All computation is wrapped
        within an mlflow run to store any run metrics, logs etc.
        """
        if self.experiment is not None:
            mlflow.set_experiment(self.experiment)

        with self.start_run() as mlflow_run:
            # Bind mlflow run to self for use in run
            self.mlflow_run = mlflow_run

            output = self.run(*args, **kwargs)

            # Unbind mlflow run
            self.mlflow_run = None

            return output


class TensorflowMixin(MLFlowMixin):
    """Tensorflow specifics to communicate with mlflow."""

    def log_model(self,
                  saved_model_dir,
                  meta_graph_tags,
                  signature_def_key,
                  artifact_path,
                  registered_model_name):
        """Log model with mlflow."""
        return mlflow.log_model(tf_saved_model_dir=saved_model_dir,
                                tf_meta_graph_tags=meta_graph_tags,
                                tf_signature_def_key=signature_def_key,
                                tf_artifact_path=artifact_path,
                                registered_model_name=registered_model_name)

    def save_model(self,
                   saved_model_dir,
                   meta_graph_tags,
                   signature_def_key,
                   path,
                   mlflow_model):
        """Save model with mlflow."""
        return mlflow.tensorflow.save_model(
            tf_saved_model_dir=saved_model_dir,
            tf_meta_graph_tags=meta_graph_tags,
            tf_signature_def_key=signature_def_key,
            path=path,
            mlflow_model=mlflow_model)

    def load_model(self, uri, session):
        """Load model with mlflow."""
        return mlflow.tensorflow.load_model(uri, session)

    def autolog(self, every_n_iter=100):
        """Log automatically (experimental in mlflow)."""
        mlflow.tensorflow.autolog(every_n_iter=every_n_iter)


# pylint: disable=abstract-method
class MLFlowProcess(Process, MLFlowMixin):
    """MLFlow Process.

    This processes generates an mlflow run and thus can log and store
    information generated at runtime. Inherit from this class if the process
    requires closer tracking by mlflow, such as model trainers and evaluators.
    """


# pylint: disable=abstract-method
class TensorflowProcess(Process, TensorflowMixin):
    """Tensorflow + MLFlow Process.

    This processes generates an mlflow run and thus can log and store
    information generated at runtime. Inherit from this class if the process
    requires closer tracking by mlflow, such as model trainers and evaluators.
    This class also provides some methods to handle storing and restoring
    tensorflow models.
    """
