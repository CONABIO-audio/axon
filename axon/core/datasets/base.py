# -*- coding: utf-8 -*-
"""Dataset Base Module.

This module defines the basic Dataset class.
"""
from abc import ABC
from abc import abstractmethod
from axon.commands.dvc import run as dvc_run, add as dvc_add


class TrackedStorage:
    """Dvc tracked storage.

    Defined as a main data output together with parameters to regenerate it
    tracking the process with dvc.
    """
    data = None
    script = None
    wdir = None
    deps = None
    outs = None
    outs_no_cache = None

    def __init__(self, data, script=None, wdir=None, deps=[], outs=[],
                 outs_no_cache=[]):
        if self.data is None:
            raise Exception("'data' can not be undefined.")
        self.data = data
        if script is not None:
            if data not in outs:
                raise Exception("'data' must be one of the outputs if 'script' \
                is defined.")
            if wdir is None:
                raise Exception("'wdir' can not be None if 'script' is \
                defined.")
            self.script = script
            self.wdir = wdir
            self.deps = deps
            self.outs = outs
            self.outs_no_cache = outs_no_cache

    def build(self, ctx):
        """Build storage.

        Parameters
        ----------
        ctx: dict
            Context for dvc and git.
        """
        if self.script is not None:
            command, result = dvc_run(ctx, self.script, self.wdir, self.deps,
                                      self.outs, self.outs_no_cache)
            print("Building storage using command: ")
            print(command)
            print("Finished! Command output: ")
            print(result)
        print("Adding data files to dvc tracking...")
        command, result = dvc_add(ctx, targets=[self.data], recursive=True)
        print("Done! Successfully added dvc tracking of " + self.data)


class Dataset(ABC):
    """Dataset Base Class.

    A dataset is an iterable object that stores objects with a definite
    datatype.
    """

    storages = None

    def __init__(self, storages):
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

    def build(self, ctx):
        """Build storages.

        Parameters
        ----------
        ctx: dict
            Context for dvc and git.
        """
        for storage in self.storages:
            storage.build(ctx)
