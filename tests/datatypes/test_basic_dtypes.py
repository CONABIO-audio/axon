# -*- coding: utf-8 -*-
"""Test module for Basic DataTypes."""
import pytest
import axon.datatypes as dt


def test_list_eq_true():
    """Check List equal method."""
    first = dt.List(dt.Float())
    second = dt.List(dt.Float())
    assert first == second

    first = dt.List(dt.Float())
    second = dt.List(dt.String())
    assert first != second


def test_list_invalid_datatype():
    """Check list validation at init."""
    with pytest.raises(ValueError, match=r"Given dtype is not a DataType. .*"):
        dt.List(int)


def test_validate_list():
    """Check whether List dtype can validate correctly."""
    dtype = dt.List(dt.Float())
    instance = [0.0, 1.2, 0.56, 8.845]
    assert dtype.validate(instance)

    dtype = dt.List(dt.Float())
    instance = [0.0, 1.2, 0.56, 8.845, 5]
    assert not dtype.validate(instance)


def test_tuple_validate():
    """Check wheter Tuple dtype can validate correctly."""
    dtype = dt.Tuple([dt.Int(), dt.String(), dt.Bool()])
    instance = [1, 'string', False]
    assert dtype.validate(instance)

    dtype = dt.Tuple([dt.Int(), dt.String(), dt.Bool()])
    instance = [1, 'string', 'false']
    assert not dtype.validate(instance)
