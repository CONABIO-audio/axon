# -*- coding: utf-8 -*-
"""Test module for pandas DataFrame DataTypes."""
import pandas as pd

import axon.datatypes as dt

def test_validate_dataframe():
    d = {'col1':[1,2], 'col2':['a', 'c'], 'col3':[0.34,5.5]}
    df = pd.DataFrame(data=d)
    D=dt.DataFrame({'col1':dt.Int(), 'col2': dt.String(), 'col3':dt.Float()}, 
                   (2,3))
    assert  D.validate(df)
    assert not D.validate(d)
    
def test_eq_data_frame():
    D=dt.DataFrame({'col1':dt.Int(), 'col2': dt.String(), 'col3':dt.Float()}, 
                   (2,3))
    E=dt.DataFrame({'col1':dt.Int(), 'col2': dt.String(), 'col3':dt.Float()}, 
                   (2,3)) 
    F=dt.DataFrame({'col1':dt.Float(), 'col2': dt.String(), 'col3':dt.Float()}, 
                   (2,3)) 
    G=dt.DataFrame({'col1':dt.Int(), 'col2': dt.String(), 'col3':dt.Float()}, 
                   (10,3)) 
    assert D==E
    assert not D==F
    assert not D==G