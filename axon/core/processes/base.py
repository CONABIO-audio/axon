# -*- coding: utf-8 -*-
"""Process Module.

This module defines the base class for all Processes.
"""
from abc import ABC
from abc import abstractmethod
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
    input_dtype = None
    output_dtype = None

    def __init__(self, input_dtype=None, output_dtype=None):
        self.logger = logging.getLogger(self.name)

        if input_dtype is None:
            input_dtype = self.input_dtype
        self._input_dtype = input_dtype

        if output_dtype is None:
            output_dtype = self.output_dtype
        self._output_dtype = output_dtype

    def get_input_dtype(self):
        """Get DataType for the input of this process.

        This method usually returns the input data type stated
        at the class declaration, or the user provided input data type at
        initialization.

        Rewrite if a more dynamic input data type setting is needed.
        """
        return self._input_dtype

    def get_output_dtype(self):
        """Get DataType for the output of this process.

        This method usually returns the output data type stated
        at the class declaration, or the user provided output data type at
        initialization.

        Rewrite if a more dynamic output data type setting is needed.
        """
        return self._output_dtype

    def info(self, *args, **kwargs):
        """Log message with info level."""
        self.logger.log(*args, **kwargs)

    def warning(self, *args, **kwargs):
        """Log message with warning level."""
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        """Log message with error level."""
        self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        """Log message with critical level."""
        self.logger.critical(*args, **kwargs)

    def run_with_dvc(self, exec_path, **kwargs):
        return dvc_run(exec_path, command=self.script, outs=self.outs,
                       deps=self.deps, **kwargs)

    @abstractmethod
    def run(self, *args, **kwargs):
        """Run the process.

        This method contains all the computation done by the process.
        It must be overwritten by the user.
        """

    def __call__(self, *args, **kwargs):
        """Run the process.

        This method is the main entrypoint to the Process. This methods
        behaviour should not be overwritten to define the process computations.
        For this use run.
        """
        return self.run(*args, **kwargs)
