# -*- coding: utf-8 -*-
"""Process module.

This module contains the definitions of a Process and their subtypes. A Process
is a single user defined unit of computation. They are meant to abstract large
chunks of computation into a reusable function.
"""
from .base import Process
from .mlflow_process import MLFlowProcess


__all__ = [
    'Process',
    'MLFlowProcess'
]
