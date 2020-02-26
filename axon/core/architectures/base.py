# -*- coding: utf-8 -*-
"""
Architecture module.

This module defines the base class for all model architectures.
"""
from abc import ABC
from axon.core.processes import Process


class ArchitectureBase(Process, ABC):  # pylint: disable=abstract-method
    """
    Architecture Base Class.

    All model architectures must inherit from this base class to standarize
    architecture behaviour.
    """
