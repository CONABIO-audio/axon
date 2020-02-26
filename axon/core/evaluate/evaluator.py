# -*- coding: utf-8 -*-
"""
Evaluator module.

This module defines the base class for all evaluation processes.
"""
from abc import ABC
from axon.core.processes import Process


class Evaluator(Process, ABC):  # pylint: disable=abstract-method
    """Evaluator class."""
