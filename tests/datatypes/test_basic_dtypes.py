# -*- coding: utf-8 -*-
"""Test module for Basic DataTypes."""
import pytest
from axon.datatypes import NoneType
from axon.datatypes import Int
from axon.datatypes import String
from axon.datatypes import Bool
from axon.datatypes import Float
from axon.datatypes import Dict
from axon.datatypes import Tuple
from axon.datatypes import List


def test_none_eq():
    """Check NoneType equal method."""
    dtype = NoneType()
    assert dtype == NoneType()
    assert dtype != Int()
    assert dtype != String()
    assert dtype != Bool()
    assert dtype != Float()


def test_none_validate():
    """Check NoneType validation method."""
    dtype = NoneType()

    variable = None
    assert dtype.validate(None)
    assert dtype.validate(variable)
    assert not dtype.validate(0)
    assert not dtype.validate(1)
    assert not dtype.validate(0.0)
    assert not dtype.validate(0.5)
    assert not dtype.validate(False)
    assert not dtype.validate(True)
    assert not dtype.validate('')
    assert not dtype.validate('string')
    assert not dtype.validate([])
    assert not dtype.validate({'key': 'value'})


def test_int_eq():
    """Check Int DataType equal method."""
    dtype = Int()
    assert dtype == Int()
    assert dtype != NoneType()
    assert dtype != String()
    assert dtype != Bool()
    assert dtype != Float()


def test_int_validate():
    """Check Int DataType validation method."""
    dtype = Int()

    assert dtype.validate(0)
    assert dtype.validate(-10)
    assert dtype.validate(10000)
    assert not dtype.validate('1')
    assert not dtype.validate(0.0)
    assert not dtype.validate(1.0)
    assert not dtype.validate(1.5)
    assert not dtype.validate('string')
    assert not dtype.validate('')
    assert not dtype.validate([])
    assert not dtype.validate({'key': 'value'})


def test_float_eq():
    """Check Float DataType equal method."""
    dtype = Float()
    assert dtype == Float()
    assert dtype != NoneType()
    assert dtype != String()
    assert dtype != Bool()
    assert dtype != Int()


def test_float_validate():
    """Check Float DataType validation method."""
    dtype = Float()

    assert dtype.validate(0.0)
    assert dtype.validate(-10.0)
    assert dtype.validate(1.5)
    assert not dtype.validate(False)
    assert not dtype.validate(True)
    assert not dtype.validate('1')
    assert not dtype.validate(0)
    assert not dtype.validate(1)
    assert not dtype.validate(-1)
    assert not dtype.validate('string')
    assert not dtype.validate('')
    assert not dtype.validate([])
    assert not dtype.validate({'key': 'value'})


def test_str_eq():
    """Check String DataType equal method."""
    dtype = String()
    assert dtype == String()
    assert dtype != NoneType()
    assert dtype != Float()
    assert dtype != Bool()
    assert dtype != Int()


def test_str_validate():
    """Check String DataType validation method."""
    dtype = String()

    assert dtype.validate('')
    assert dtype.validate('1')
    assert dtype.validate('string')
    assert not dtype.validate(False)
    assert not dtype.validate(True)
    assert not dtype.validate(0.0)
    assert not dtype.validate(0)
    assert not dtype.validate(1)
    assert not dtype.validate(-1)
    assert not dtype.validate(1.2)
    assert not dtype.validate(-2.3)
    assert not dtype.validate([])
    assert not dtype.validate({'key': 'value'})


def test_bool_eq():
    """Check Bool DataType equal method."""
    dtype = Bool()
    assert dtype == Bool()
    assert dtype != NoneType()
    assert dtype != Float()
    assert dtype != String()
    assert dtype != Int()


def test_bool_validate():
    """Check Bool DataType validation method."""
    dtype = Bool()

    assert dtype.validate(True)
    assert dtype.validate(False)
    assert not dtype.validate('')
    assert not dtype.validate('string')
    assert not dtype.validate(0.0)
    assert not dtype.validate(0)
    assert not dtype.validate(1)
    assert not dtype.validate(-1)
    assert not dtype.validate(1.2)
    assert not dtype.validate(-2.3)
    assert not dtype.validate([])
    assert not dtype.validate({'key': 'value'})


def test_list_eq():
    """Check List equal method."""
    float_list = List(Float())
    int_list = List(Int())

    assert float_list == List(Float())
    assert int_list == List(Int())
    assert float_list != [1.0, 2.0]
    assert float_list != 1.3
    assert float_list != int_list
    assert float_list != Int()
    assert float_list != Float()
    assert float_list != NoneType()
    assert float_list != Tuple([Float()])
    assert float_list != Dict({'key': Float()})
    assert float_list != List(Bool())
    assert float_list != List(String())


def test_list_init():
    """Check list validation at init."""
    with pytest.raises(ValueError, match=r"Given dtype is not a DataType. .*"):
        List(int)


def test_list_validate():
    """Check whether List dtype can validate correctly."""
    float_list = List(Float())
    int_list = List(Int())
    bool_list = List(Bool())
    str_list = List(String())

    assert float_list.validate([])
    assert float_list.validate([0.0, 1.2, 0.56, 8.845])
    assert int_list.validate([])
    assert int_list.validate([1, 2, 3])
    assert bool_list.validate([])
    assert bool_list.validate([True, False, True])
    assert str_list.validate([])
    assert str_list.validate(['1', '2', '3'])
    assert not float_list.validate([0.0, 1.2, 0.56, 8.845, 5])
    assert not float_list.validate(1.2)
    assert not float_list.validate([False])
    assert not int_list.validate([1, 2, 'a'])
    assert not int_list.validate(1)
    assert not bool_list.validate([False, 2])
    assert not bool_list.validate(False)
    assert not str_list.validate('string')
    assert not str_list.validate(['string', False])


def test_dict_init():
    """Check dict validation at init."""
    with pytest.raises(ValueError):
        Dict(String())

    with pytest.raises(ValueError):
        Dict({'key': 0})

    with pytest.raises(ValueError):
        Dict({'key': str})


def test_dict_eq():
    """Check Dict DateType equal method."""
    float_dict = Dict({'a': Float()})
    int_dict = Dict({'a': Int()})

    assert float_dict == Dict({'a': Float()})
    assert int_dict == Dict({'a': Int()})
    assert float_dict != Dict({'b': Float()})
    assert float_dict != Dict({'a': Float(), 'b': Float()})
    assert float_dict != {'a': 1.0}
    assert float_dict != int_dict
    assert float_dict != {}
    assert float_dict != String()
    assert float_dict != Int()
    assert float_dict != Bool()
    assert float_dict != Float()
    assert float_dict != NoneType()
    assert int_dict != Dict({'b': Int()})
    assert int_dict != Dict({'a': Int(), 'b': Int()})
    assert int_dict != {'a': 1}
    assert int_dict != String()
    assert int_dict != Int()
    assert int_dict != Bool()
    assert int_dict != Float()
    assert int_dict != NoneType()
    assert int_dict != List(Int())
    assert int_dict != Tuple([Int()])


def test_dict_validate():
    """Check Dict DateType validate method."""
    float_dict = Dict({'a': Float()})
    int_dict = Dict({'a': Int()})

    assert float_dict.validate({'a': -10.5})
    assert float_dict.validate({'a': 0.0})
    assert float_dict.validate({'a': 10.5})
    assert int_dict.validate({'a': -1})
    assert int_dict.validate({'a': 0})
    assert int_dict.validate({'a': 1})
    assert not float_dict.validate({'a': 1.0, 'b': 1.0})
    assert not float_dict.validate({'a': 1})
    assert not float_dict.validate({'b': 1.0})
    assert not float_dict.validate({'a': False})
    assert not float_dict.validate({'a': 'string'})
    assert not float_dict.validate(1.0)
    assert not float_dict.validate([1.0, 2.0])
    assert not int_dict.validate({'a': 1, 'b': 1})
    assert not int_dict.validate({'a': 1.0})
    assert not int_dict.validate({'b': 1})
    assert not int_dict.validate({'a': 'string'})
    assert not int_dict.validate(1)
    assert not int_dict.validate([1, 2])


def test_tuple_init():
    """Check validation at Tuple init."""
    with pytest.raises(ValueError):
        Tuple(0)

    with pytest.raises(ValueError):
        Tuple(str)

    with pytest.raises(ValueError):
        Tuple({})

    with pytest.raises(ValueError):
        Tuple([str])

    with pytest.raises(ValueError):
        Tuple((str, int))

    with pytest.raises(ValueError):
        Tuple((String(), int))


def test_tuple_validate():
    """Check wheter Tuple dtype can validate correctly."""
    int_tuple = Tuple([Int()])
    str_tuple = Tuple([String()])
    compound_tuple = Tuple([Int(), String()])

    assert int_tuple.validate([1])
    assert int_tuple.validate((0,))
    assert str_tuple.validate(['string'])
    assert str_tuple.validate(('string',))
    assert compound_tuple.validate([1, 'string'])
    assert compound_tuple.validate((1, 'string'))

    assert not int_tuple.validate(1)
    assert not int_tuple.validate([1, 2])
    assert not int_tuple.validate({'a': 1})
    assert not int_tuple.validate([1.0])
    assert not int_tuple.validate(['string'])
    assert not int_tuple.validate([])

    assert not str_tuple.validate('string')
    assert not str_tuple.validate(['string1', 'string2'])
    assert not str_tuple.validate({'key': 'string'})
    assert not str_tuple.validate([1])
    assert not str_tuple.validate([False])
    assert not str_tuple.validate([])

    assert not compound_tuple.validate(100)
    assert not compound_tuple.validate(['string1', 'string2'])
    assert not compound_tuple.validate([1, 2])
    assert not compound_tuple.validate([1, 'string', 3])
    assert not compound_tuple.validate({1: 1, 2: 'string'})
    assert not compound_tuple.validate([1])
    assert not compound_tuple.validate([False])
    assert not compound_tuple.validate([])


def test_tuple_eq():
    """Check Tuple eq method."""
    int_tuple = Tuple([Int()])
    str_tuple = Tuple([String()])
    compound_tuple = Tuple([Int(), String()])

    assert int_tuple == Tuple((Int(),))
    assert str_tuple == Tuple((String(),))
    assert compound_tuple == Tuple((Int(), String()))
    assert int_tuple != str_tuple
    assert int_tuple != compound_tuple
    assert str_tuple != compound_tuple
    assert int_tuple != (1, )
    assert str_tuple != ('string', )
    assert compound_tuple != (1, 'string')
    assert int_tuple != NoneType()
    assert int_tuple != String()
    assert int_tuple != Int()
    assert int_tuple != Float()
    assert int_tuple != Dict({'key': Int()})
    assert int_tuple != List(Int())
    assert int_tuple != Bool()


def test_conjunction_init():
    """Check conjunction validation at init."""
    with pytest.raises(ValueError):
        _ = String() | int

    with pytest.raises(ValueError):
        _ = int | String()


def test_conjunction_eq():
    """Check conjunction eq method."""
    int_or_str = Int() | String()
    int_or_bool = Int() | Bool()
    float_or_str = Float() | String()

    assert int_or_str == Int() | String()
    assert int_or_str == String() | Int()
    assert int_or_bool == Int() | Bool()
    assert int_or_bool == Bool() | Int()
    assert float_or_str == Float() | String()
    assert float_or_str == String() | Float()
    assert int_or_str != int_or_bool
    assert int_or_str != float_or_str
    assert int_or_bool != float_or_str
    assert int_or_str != Int()
    assert int_or_str != int
    assert int_or_str != 0
    assert int_or_str != 'string'
    assert int_or_str != String()
    assert int_or_str != NoneType()
    assert int_or_str != Tuple([Int(), String()])
    assert int_or_str != List(Int())
    assert int_or_str != Dict({'a': Int(), 'b': String()})


def test_conjunction_validate():
    """Check conjunction eq method."""
    int_or_str = Int() | String()
    int_or_bool = Int() | Bool()
    float_or_str = Float() | String()

    assert int_or_str.validate(-1)
    assert int_or_str.validate(0)
    assert int_or_str.validate(1)
    assert int_or_str.validate('')
    assert int_or_str.validate('string')
    assert not int_or_str.validate([1, 'string'])
    assert not int_or_str.validate([])
    assert not int_or_str.validate(1.0)
    assert not int_or_str.validate({1: 0, 2: 'string'})

    assert int_or_bool.validate(-1)
    assert int_or_bool.validate(0)
    assert int_or_bool.validate(1)
    assert int_or_bool.validate(True)
    assert int_or_bool.validate(False)
    assert not int_or_bool.validate([1, True])
    assert not int_or_bool.validate([])
    assert not int_or_bool.validate(1.0)
    assert not int_or_bool.validate('string')
    assert not int_or_bool.validate({1: 0, 2: True})

    assert float_or_str.validate(-1.5)
    assert float_or_str.validate(0.0)
    assert float_or_str.validate(1.5)
    assert float_or_str.validate('')
    assert float_or_str.validate('string')
    assert not float_or_str.validate([1.0, 'string'])
    assert not float_or_str.validate([])
    assert not float_or_str.validate(False)
    assert not float_or_str.validate(1)
    assert not float_or_str.validate({1: 1.0, 2: 'string'})
