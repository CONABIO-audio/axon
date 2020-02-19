"""Package tests"""
import pytest
import numpy as np
"""Datatype tests"""
import axon.datatypes.base as dt

def test_List_eq_True():
    A=dt.List(dt.Float())
    B=dt.List(dt.Float())
    assert (A==B) == True
    
def test_List_eq_False():
    A=dt.List(dt.Float())
    B=dt.List(dt.String())
    assert (A==B) == False

def test_List_invalid_Datatype():
    with pytest.raises(ValueError, match=r"Given dtype is not a DataType. .*"):
        lnot=dt.List(int)
        
def test_validate_list():
    A=dt.List(dt.Float())
    B=[0.0,1.2,0.56, 8.845]
    assert (A.validate(B))==True
    
def test_validate_list_bad():
    A=dt.List(dt.Float())
    B=[0.0,1.2,0.56, 8.845,5]
    assert (A.validate(B))==False   

def test_Tuple_validate():
    A=dt.Tuple([dt.Int(), dt.String(), dt.Bool()])
    B=[1, 'string', False]
    assert(A.validate(B))==True
    
def test_Tuple_validate_bad():
    A=dt.Tuple([dt.Int(), dt.String(), dt.Bool()])
    B=[1, 'string', 'false']
    assert(A.validate(B))==False

def test_npArray():
    A=dt.NumpyArray(dt.Float(), (240,240))
    B= np.eye(240)
    assert (A.validate(B))==True
    
def test_npArray_bad1():
    A=dt.NumpyArray(dt.Int(), (240,240))
    B= np.eye(240)
    assert (A.validate(B))==False    
    
def test_npArray_compare():
    A=dt.NumpyArray(dt.Int(), (240,240))
    B= dt.NumpyArray(dt.Int(), (240,240))
    assert (A==B)==True     
    
def test_npArray_comparebad():
    A=dt.NumpyArray(dt.Int(), (240,240))
    B= dt.NumpyArray(dt.Int(), (240,239))
    assert (A==B)==False    
    
def test_npArray_comparebad2():
    A=dt.NumpyArray(dt.Int(), (240,240))
    B= dt.NumpyArray(dt.Float(), (240,240))
    assert (A==B)==False 