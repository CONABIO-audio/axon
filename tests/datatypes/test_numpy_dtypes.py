# -*- coding: utf-8 -*-
"""Test module for Numpy DataTypes."""
import numpy as np

import axon.datatypes as dt


def test_np_array():
    """Check numpy array can validate correctly."""
    dtype = dt.NumpyArray(dt.Float(), (240, 240))
    instance = np.eye(240)
    assert dtype.validate(instance)

    dtype = dt.NumpyArray(dt.Int(), (240, 240))
    instance = np.eye(240)
    assert not dtype.validate(instance)


def test_np_array_compare():
    """Check numpy arrays dtypes when equal."""
    first = dt.NumpyArray(dt.Int(), (240, 240))
    second = dt.NumpyArray(dt.Int(), (240, 240))
    assert first == second


def test_np_array_comparebad():
    """Check numpy array dtype when unequal."""
    first = dt.NumpyArray(dt.Int(), (240, 240))
    second = dt.NumpyArray(dt.Int(), (240, 239))
    assert first != second

    first = dt.NumpyArray(dt.Int(), (240, 240))
    second = dt.NumpyArray(dt.Float(), (240, 240))
    assert first != second
