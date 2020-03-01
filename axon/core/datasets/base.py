# -*- coding: utf-8 -*-
"""Dataset Base Module.

This module defines the basic Dataset class.
"""
from abc import ABC
from abc import abstractmethod
from axon.commands.dvc import add as dvc_add


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

    def __init__(self, data, script=None, wdir=None, deps=None, outs=None,
                 outs_no_cache=None):
        if self.data is None:
            raise Exception("'data' can not be undefined.")

        self.data = data

        if script is None:
            return

        if self.data not in outs:
            raise Exception("'data' must be one of the outputs if 'script' \
            is defined.")
        if wdir is None:
            raise Exception("'wdir' can not be None if 'script' is \
            defined.")

        self.script = script
        self.wdir = wdir

        if deps is not None:
            self.deps = deps

        if outs is not None:
            self.outs = outs

        if outs_no_cache is not None:
            self.outs_no_cache = outs_no_cache

    def build(self, exec_path):
        """Build storage.

        Parameters
        ----------
        ctx: dict
            Context for dvc and git.
        """
        if self.process is not None:
            command, result = self.process.run_with_dvc(exec_path)
            print("Building storage using command: ")
            print(command)
            print("Finished! Command output: ")
            print(result)
        print("Adding data files to dvc tracking...")
        command, result = dvc_add(exec_path, targets=[self.data],
                                  recursive=True)
        print("Done! Successfully added dvc tracking of " + self.data)


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

    def build(self, exec_path):
        """Build storages.

        Parameters
        ----------
        ctx: dict
            Context for dvc and git.
        """
        for storage in self.storages:
            storage.build(exec_path)


### bat_detector/scripts/generate_metadata.py

class GenerateMetadata(Process):
    outs = [
        'metadata.sqlite',
        'metadata_process.log',
        'samples.npy'
    ]
    wdir = 'data/metadata/'

    def run(self):
        return 1

### Consola

### bat_detector/datasets/bat_dataset.py

class BatDataset(Dataset):
    storages = {
        'metadata': TrackedStorage(
            data='metadata.sqlite',
            script='bat_detector.scripts.generate_metadata')
    }

    def get(self):
        metadata_path = self.get_storage_path('metadata')
