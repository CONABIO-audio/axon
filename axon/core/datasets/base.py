# -*- coding: utf-8 -*-
"""Dataset Base Module.

This module defines the basic Dataset class.
"""
from abc import ABC
from abc import abstractmethod
from axon.core.processes import Process


class TrackedStorage:
    """Dvc tracked storage.

    Defined as a main data output together with parameters to regenerate it
    tracking the process with dvc.
    """

    data = None
    process = None

    def __init__(self, data, process=None):
        if self.data is None:
            raise ValueError("'data' must be defined.")

        self.data = data

        if process is not None:
            self.process = process

        if self.process is None:
            return

        if not isinstance(self.process, Process):
            message = "The provided process is not of the right type \
            (type ={})."
            message = message.format(type(self.process))

        if self.data not in self.process.outputs:
            raise Exception("'data' must be one of the outputs if 'process' \
            is defined.")


class Dataset(ABC):
    """Dataset Base Class.

    A dataset is an iterable object that stores objects with a definite
    datatype.
    """

    storages = None

    def __init__(self, storages=None):
        if storages is not None:
            self.storages = storages

    @abstractmethod
    def iter(self):
        """Construct an iterator for the dataset contents."""

    @abstractmethod
    def len(self):
        """Return the length of this dataset."""

    @abstractmethod
    def get(self, uid):
        """Return example with uid.

        Parameters
        ----------
        uid: str
            Unique identifier of data element to retrieve.

        Returns
        -------
        data: list
            Match as only element or empty list.
        """
