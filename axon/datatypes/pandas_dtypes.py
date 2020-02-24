# -*- coding: utf-8 -*-
"""
Pandas dataframe DataTypes module.

Pandas dataframes as DataTypes are defined in this module.
"""
import pandas as pd
from axon.datatypes.base import DataType


class DataFrame(DataType):
    """Pandas dataframe DataType.

    We create a class for pandasdataframes. At initialization the
    column names and the DataType of the entries must be defined
    in a dictionary.

    Examples
    --------
    DataFrame({'col1': Float(), 'col2':Int()})
    """

    def __init__(self, dtypes_dict, **kwargs):
        # Verify description of dataframe is a dictionary
        if not isinstance(dtypes_dict, dict):
            message = "Description of dataframe should be a dictionary"
            raise ValueError(message)

        # Verify the DataTypes for the values are valid DataTypes.
        for value in dtypes_dict.values():
            if not isinstance(value, DataType):
                message = 'Given dtype is not a DataType. (type={})'
                message = message.format(type(value))
                raise ValueError(message)
        super().__init__(**kwargs)
        self.pandas_dict = dtypes_dict

    def validate(self, other):
        """Check if argument is a pandas DataFrame of this type."""
        # Verify instance is a pdndas dataframe
        if not isinstance(other, pd.DataFrame):
            return False
        # Verify column names are correct
        for key, value in self.pandas_dict.items():
            if key not in other.columns:
                return False
            for entry in other[key]:
                if not value.validate(entry):
                    return False
        return True

    def __eq__(self, other):
        """Check if other is the same NumpyArray DataType."""
        if not isinstance(other, DataFrame):
            return False
        # Verify column names are correct
        for key, value in self.pandas_dict.items():
            if key not in other.pandas_dict:
                return False

            if value != other.pandas_dict[key]:
                return False

        # Check if there are keys in instance that are not
        # in the defined dtype
        for key in other.pandas_dict:
            if key not in self.pandas_dict:
                return False

        return True

    def __repr__(self):
        """Get full representation."""
        return 'DataFrame({}, {})'.format(
            dict.__repr__(self.pandas_dict))

    def __str__(self):
        """Get string representation."""
        str_dict = {
            key: str(value)
            for key, value in self.pandas_dict.items()
        }
        return str(str_dict)
