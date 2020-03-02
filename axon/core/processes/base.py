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
    wdir = None

    deps = []
    outs = []
    outs_no_cache = []
    metrics_no_cache = []
    metrics = []

    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(self.name)
        self.config_logging()

    def config_logging(self):
        """Configure the process logger."""

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
