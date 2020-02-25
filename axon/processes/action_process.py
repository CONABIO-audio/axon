# -*- coding: utf-8 -*-
"""
Action process Module.

This module defines the base class for all action processes. In its most
simple usage, an action process can be built from a python function.
"""

from axon.processes.base import Process


class ActionProcess(Process):
    """Action process base class.

    An action process is a Process that accepts a method with compatible inputs
    and outputs to be used in internal run method.
    """

    action = None

    def __init__(self, action=None, **kwargs):
        self.set_action(action)
        super().__init__(**kwargs)

    def set_action(self, action=None):
        """Specify internal action for actual computation."""
        if action is not None:
            self.action = action

    def get_action(self):
        """Return process action."""
        return self.action

    def run(self, *args, **kwargs):
        """Run action."""
        if self.action is not None:
            return self.action(*args, **kwargs)
        return None
