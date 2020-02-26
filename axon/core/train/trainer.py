# -*- coding: utf-8 -*-
"""
Trainer module.

In this module the base class for al Trainer processes is defined.
"""
from abc import ABC
from axon.core.processes import Process


class Trainer(Process, ABC):  # pylint: disable=abstract-method
    """
    Trainer base class.

    All training processes must inherit from this class.
    """
