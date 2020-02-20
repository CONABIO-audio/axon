# -*- coding: utf-8 -*-
"""
Pandas dataframe DataTypes module.

Pandas dataframes as DataTypes are defined in this module.
"""
#import pandas as pd
from axon.datatypes.base import DataType
class DataFrame(DataType):
    def __init__(self, dtypes_dict, shape, **kwargs):
        
        # Verify description of dataframe is a dictionary
        if not isinstance(dtypes_dict, dict):
            message = "Description of dataframe should be a dictionary"
            message = message +"." (arg={})
            message = message.format(dtypes_dict)
            raise ValueError(message)

        # Verify the DataTypes for the values are valid DataTypes.
        for value in dtypes_dict.values():
            if not isinstance(value, DataType):
                message = 'Given dtype is not a DataType. (type={})'
                message = message.format(type(value))
                raise ValueError(message)
        
        # Verify shape is specified as a tuple or list
        if not isinstance(shape, (tuple, list)):
            message = 'Shape should be given as a tuple. (type={})'
            message = message.format(type(shape))
            raise ValueError(message)

        # Verify shape has integer values
        for item in shape:
            if not isinstance(item, int):
                message = ('All entries of shape should be of type int.')            
                raise ValueError(message)

        super().__init__(**kwargs)
        self.pandas_dict=dtypes_dict
        self.shape=shape
        
    def validate(self, other):
        
        pass
