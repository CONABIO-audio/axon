# -*- coding: utf-8 -*-
"""Dataset Base Module.

This module defines the basic Dataset class.
"""
from abc import ABC
from abc import abstractmethod


class Dataset(ABC):
    """Dataset Base Class.

    A dataset is an iterable object that stores objects with a definite
    datatype.
    """

    datum_datatype = None

    @abstractmethod
    def iter(self):
        """Construct an iterator for the dataset contents."""

    @abstractmethod
    def len(self):
        """Return the length of the dataset."""
