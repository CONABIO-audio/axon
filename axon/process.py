# -*- coding: utf-8 -*-
"""Process Module.

This module defines the base class for all Processes.
"""
from abc import ABC
from abc import abstractmethod
import logging


class Process(ABC):
    """Process base class."""

    name = None

    def __init__(self):
        self.logger = logging.getLogger(self.name)

    def info(self, *args, **kwargs):
        """Log message with info level."""
        self.logger.log(*args, **kwargs)

    def warning(self, *args, **kwargs):
        """Log message with warning level."""
        self.logger.warning(*args, **kwargs)

    def error(self, *args, **kwargs):
        """Log message with error level."""
        self.logger.error(*args, **kwargs)

    def critical(self, *args, **kwargs):
        """Log message with critical level."""
        self.logger.critical(*args, **kwargs)

    @abstractmethod
    def run(self, *inputs, **kwargs):
        """Run the process.

        This method contains all the computation within the process.
        It must be overwritten by the user.
        """
