# -*- coding: utf-8 -*-
"""
Numpy DataTypes module.

All data types of numpy arrays are defined in this module.
"""
import numpy as np
from axon.datatypes.base import DataType


class NumpyArray(DataType):
    """Numpy array DataType.

    We create a class for multidimension numpy arrays. At initialization the
    DataType of the entries must be defined as well as the shape of the numpy
    array.

    Examples
    --------
    NumpyArray(Float(), (2,2))
    """

    def __init__(self, dtype, shape, **kwargs):
        """Create a Numpy Array DataType."""
        # Verify dtype is a valid DataType
        if not isinstance(dtype, DataType):
            message = 'Given dtype is not a DataType. (type={})'
            message = message.format(type(dtype))
            raise ValueError(message)

        # Verify shape is specified as a tuple or list
        if not isinstance(shape, (tuple, list)):
            message = 'Shape should be given as a tuple. (type={})'
            message = message.format(type(dtype))
            raise ValueError(message)

        # Verify shape has integer values
        for item in shape:
            if not isinstance(item, int):
                message = ('All entries of shape should be of type int.')
                raise ValueError(message)

        super().__init__(**kwargs)

        self.nparray_item_type = dtype
        self.shape = shape

    def validate(self, other):
        """Check if argument is a Numpy Array of this type."""
        # Verify instance is a np array
        if not isinstance(other, np.ndarray):
            return False

        # Verify shape is correct
        if not self.shape == other.shape:
            return False

        # Verify all entries correspond to the correct DataType
        aux = other.reshape(np.prod(other.shape))
        for item in aux:
            if not self.nparray_item_type.validate(item):
                return False
        return True

    def __eq__(self, other):
        """Check if other is the same NumpyArray DataType."""
        if not isinstance(other, DataType):
            return False

        # Verify it is a list from attribute nparray_item_type
        if not hasattr(other, 'nparray_item_type'):
            return False

        if not self.shape == other.shape:
            return False

        return self.nparray_item_type == other.nparray_item_type

    def __repr__(self):
        """Get full representation."""
        return 'NumpyArray({})'.format(repr(self.nparray_item_type))

    def __str__(self):
        """Get string representation."""
        return 'NumpyArray({})'.format(str(self.nparray_item_type))
