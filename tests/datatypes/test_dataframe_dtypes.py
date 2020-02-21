# -*- coding: utf-8 -*-
"""Test module for pandas DataFrame DataTypes."""
import pandas as pd

import axon.datatypes as dt

def test_validate_dataframe():
    d = {'col1':[1,2], 'col2':['a', 'c'], 'col3':[0.34,5.5]}
    df = pd.DataFrame(data=d)
    D=dt.DataFrame({'col1':dt.Int(), 'col2': dt.String(), 'col3':dt.Float()}, (2,3))
    assert  D.validate(df)
    assert not D.validate(d)
