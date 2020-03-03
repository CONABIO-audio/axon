# -*- coding: utf-8 -*-
"""Process Module.

This module defines the base class for all Processes.
"""
from abc import ABC
from abc import abstractmethod
from copy import copy
import os
import logging


class Process(ABC):
    """Process base class.

    A process is any data transformation function. All process must have a
    name and should also declare input and output datatypes
    using axon datatype API.

    All computation done by the process should be defined in the run method.

    Examples
    --------
    To create a process that generates spectrograms from the wav numpy array,
    one could define:

    .. code-block:: python
        import numpy as np
        import librosa

        from axon.process import Process
        import axon.datatypes as dtypes


        class SpectrogramMaker(Process):
            name = 'Spectrogram Maker'
            input_dtype = dtypes.NumpyArray(np.float, [None])
            output_dtype = dtypes.NumpyArray(np.float, [513, None])

            def run(self, wav):
                spec = np.abs(librosa.core.stft(wav, n_fft=1024)
                return spec
    """

    name = None
    deps = None
    outs = None
    metrics = None
    metrics_no_cache = None
    outs_no_cache = None
    wdir = None

    def __init__(self, config=None, wdir=None):
        self.log = logging.getLogger(self.name)

        if config is None:
            config = {}
        self.config = config

        if self.wdir is None and wdir is not None:
            self.wdir = wdir

        if self.wdir is not None and not isinstance(self.wdir, str):
            message = (
                'The specified working directory for this process is not '
                'a string')
            raise ValueError(message)

        if self.deps is not None and not isinstance(self.deps, dict):
            message = (
                'The specified dependencies for this process are not '
                'in a dictionary')
            raise ValueError(message)

        if self.outs is not None and not isinstance(self.outs, dict):
            message = (
                'The specified outputs for this process are not '
                'in a dictionary')
            raise ValueError(message)

        if self.outs_no_cache is not None and not isinstance(self.outs_no_cache, dict):  # noqa
            message = (
                'The specified outputs no cache for this process are not '
                'in a dictionary')
            raise ValueError(message)

        if self.metrics is not None and not isinstance(self.metrics, dict):
            message = (
                'The specified metrics for this process are not '
                'in a dictionary')
            raise ValueError(message)

        if self.metrics_no_cache is not None and not isinstance(self.metrics_no_cache, dict):  # noqa
            message = (
                'The specified metrics no cache for this process are not '
                'in a dictionary')
            raise ValueError(message)

    @abstractmethod
    def run(self, *args, **kwargs):
        """Run the process.

        This method contains all the computation done by the process.
        It must be overwritten by the user.
        """

    def get_out_path(self, name):
        """Get the correct path for the output file."""
        if self.outs is None:
            outs = {}
        else:
            outs = copy(self.outs)

        if self.outs_no_cache is None:
            outs_no_cache = {}
        else:
            outs_no_cache = copy(self.outs_no_cache)

        outs.update(outs_no_cache)

        if len(outs) == 0:
            message = 'No otuputs where specified for this process'
            raise ValueError(message)

        if name not in outs:
            message = (
                f'No output with name {name} was specified for this'
                ' process')
            raise ValueError(message)

        relative_path = outs[name]

        if self.wdir is not None:
            os.path.join(self.wdir, relative_path)

        return relative_path

    def get_metric_path(self, name):
        """Get the correct path for the metric file."""
        if self.metrics is None:
            metrics = {}
        else:
            metrics = copy(self.metrics)

        if self.metrics_no_cache is None:
            metrics_no_cache = {}
        else:
            metrics_no_cache = copy(self.metrics_no_cache)

        metrics.update(metrics_no_cache)

        if len(metrics) == 0:
            message = 'No metrics where specified for this process'
            raise ValueError(message)

        if name not in metrics:
            message = (
                f'No metric with name {name} was specified for this'
                ' process')
            raise ValueError(message)

        relative_path = metrics[name]

        if self.wdir is not None:
            os.path.join(self.wdir, relative_path)

        return relative_path

    def get_dep_path(self, name):
        """Get the correct path for the dependency file."""
        deps = self.deps
        if deps is None:
            deps = {}

        if len(deps) == 0:
            message = 'No dependencies where specified for this process'
            raise ValueError(message)

        if name not in deps:
            message = (
                f'No dependency with name {name} was specified for this'
                ' process')
            raise ValueError(message)

        relative_path = deps[name]

        if self.wdir is not None:
            os.path.join(self.wdir, relative_path)

        return relative_path

    def get_dependencies(self):
        """Get all process dependency paths."""
        if self.deps is None:
            return []

        return [self.get_dep_path(key) for key in self.deps]

    def get_outs(self):
        """Get all process output paths."""
        if self.outs is None:
            return []

        return [self.get_out_path(key) for key in self.outs]

    def get_outs_no_cache(self):
        """Get all process no cached output paths."""
        if self.outs_no_cache is None:
            return []

        return [self.get_out_path(key) for key in self.outs_no_cache]

    def get_metrics(self):
        """Get all process metric paths."""
        if self.metrics is None:
            return []

        return [self.get_metric_path(key) for key in self.metrics]

    def get_metrics_no_cache(self):
        """Get all process no cached metric paths."""
        if self.metrics_no_cache is None:
            return []

        return [self.get_metric_path(key) for key in self.metrics_no_cache]

    def __call__(self, *args, **kwargs):
        """Run the process.

        This method is the main entrypoint to the Process. This methods
        behaviour should not be overwritten to define the process computations.
        For this use run.
        """
        return self.run(*args, **kwargs)
