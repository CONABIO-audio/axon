# -*- coding: utf-8 -*-
"""
torch.nn.module process Module.

This module defines the base class for all processes with actions defined as a
torch.nn.module. It is intended to be used for evaluation as well as training
changing between both modalities using the "set_mode" method.
"""

from axon.processes import ParametrizedProcess


class TorchNnModuleProcess(ParametrizedProcess):
    """Base class for any process whose action is a torch.nn.module.

    Setting mode to "train" changes the behaviour of "run" producing outputs
    that are usable by a trainer built for torch.
    """

    mode = "eval"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_mode(self.mode)

    def set_mode(self, mode="eval"):
        if mode == "eval":
            self.action.eval()
        else:
            self.action.train()
