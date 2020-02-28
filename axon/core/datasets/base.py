# -*- coding: utf-8 -*-
"""Dataset Base Module.

This module defines the basic Dataset class.
"""
from abc import ABC
from abc import abstractmethod
from axon.commands.dvc import run as dvc_run


class Dataset(ABC):
    """Dataset Base Class.

    A dataset is an iterable object that stores objects with a definite
    datatype.
    """

    datum_datatype = None
    build_commands = []
    data = []

    @abstractmethod
    def iter(self):
        """Construct an iterator for the dataset contents."""

    @abstractmethod
    def len(self):
        """Return the length of the dataset."""

    @abstractmethod
    def get(self, uid):
        """Return example with uid."""

    def build(self):
        dvc_run(self.build_command)




### 
class TrainingDataset(Dataset):
    data = [
        'data/species/species1.tfrecords',
        'data/species/species2.tfrecords',
        'data/noise.tfrecords',
        'data/agumentations/species1.tfrecords',
        'data/metadata.sqlite',
    ]

    build_commands = [
        'bat_detector.scripts.make_species_tfrecords',
        'bat_detector.scripts.generate_false_data',
        'bat_detector.'
    ]

    def __init__(self):
        self.species1 = self.load('data/species/species1.tfrecords')
        self.species2 = self.load('data/species/species2.tfrecords')
        self.noise = self.load('data/noise.tfrecords')
        self.artificial = self.load('data/augmentations/model1.tfrecords')
        self.metadata = self.load('data/metadata.sqlite')

    def iter(self):
        return self.interlace(self.species1, self.species2, self.noise)
