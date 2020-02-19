"""
DataType Module.

All DataTypes and utility functions are importable from this module.
A DataType is an object used to describe the contents of a DataObject
and can be used to specify the signatures of processes and functions.

They serve as a mechanism for type checking on pipeline construction
and as documentation.
"""
from .base import DataType
from .base import Int
from .base import Float
from .base import String
from .base import Bool
from .base import List
from .base import Tuple
from .base import Dict


__all__ = [
    'DataType',
    'Int',
    'Float',
    'String',
    'Bool',
    'List',
    'Tuple',
    'Dict',
]

# TODO: Implementar Numpy Array
# TODO: Implementar DataFrame
