"""
DataType base module.

Here we define the different datatype classes. Each DataType has a method
to validate that an instance corresponds to that DataType and a method
to compare if two DataTypes have the same structure.
These features will be useful to verify whether an input of a process has
the correct datatype and structure.
"""
from abc import ABC
from abc import abstractmethod
import numpy as np

class DataType(ABC):
    """
    The Datatype base class.

    Has the validate and __eq__ methods. Since validate
    is an abstract method it must be redefined for every data type accordingly.
    """

    @abstractmethod
    def validate(self, other):
        """Check if object is of this datatype."""

    def __eq__(self, other):
        """Check if two datatypes are the same."""
        return isinstance(other, type(self))


class Tuple(DataType):
    """
    The Tuple DataType.

    The tuple datatype is an array of a fixed length and every entry may be
    a different Datatype.
    To initialize a Tuple an array with the DataTypes of each entry must be
    given.

    Example: Tuple([Int(), Bool(), String()])
    """

    def __init__(self, type_array):
        """Create a Tuple from list of datatypes."""
        # Verify if the entries correspond to an accepted DataType
        for dtype in type_array:
            if not isinstance(dtype, DataType):
                message = 'Array value is not a DataType. (type={})'
                message = message.format(type(dtype))
                raise ValueError(message)

        # Define attribute tuple_data_type
        self.tuple_data_types = type_array

    def validate(self, other):
        """Check if argument is a Tuple."""
        # Verify if other is a tuple or list
        if not isinstance(other, (tuple, list)):
            return False

        # Check if length of the defined tuple coincides with other's length
        if len(other) != len(self.tuple_data_types):
            return False

        # Verify that the datatypes coincide in each entry
        for other_item, array_dtype in zip(other, self.tuple_data_types):
            if not array_dtype.validate(other_item):
                return False

        return True

    def __eq__(self, other):
        # Check DataType is valid
        if not isinstance(other, DataType):
            return False

        # Verify it is a tuple by checking the attribute tuple_data_types
        # is present
        if not hasattr(other, 'tuple_data_types'):
            return False

        # Check if lengths coincide
        if len(self.tuple_data_types) != len(other.tuple_data_types):
            return False

        # Verify that the datatypes coincide in each entry
        for self_dtype, other_dtype in zip(
                self.tuple_data_types,
                other.tuple_data_types):
            if not self_dtype == other_dtype:
                return False

        return True

    def __repr__(self):
        reprs = tuple([repr(dtype) for dtype in self.tuple_data_types])
        return 'Tuple({})'.format(repr(reprs))

    def __str__(self):
        strs = tuple([str(dtype) for dtype in self.tuple_data_types])
        return str(strs)


class Dict(DataType):
    """
    Dictionary Datatype.

    To define a Dict one must include the structure of the dictionary with
    its corresponding keys and DataType for each key.
    Example: Dict({'Key1':Int(), 'Key2':Bool()})
    """

    def __init__(self, dict_struct):
        """Create a Dict DataType from dictionary of DataTypes."""
        # Verify the DataTypes for the values are valid DataTypes.
        for value in dict_struct.values():
            if not isinstance(value, DataType):
                message = 'Dictionary value is not a DataType. (type={})'
                message = message.format(type(value))
                raise ValueError(message)

        self.dict_dtypes = dict_struct

    def validate(self, other):
        """Check if argument is of this Dict type."""
        if not isinstance(other, dict):
            return False

        # Check if every key in the defined class is present
        # in the other instance.
        # And check if the values for a given key coincide in both.
        for key, value in self.dict_dtypes.items():
            if key not in other:
                return False
            if not value.validate(other[key]):
                return False

        return True

    def __eq__(self, other):
        # Check if it is a valid DataType
        if not isinstance(other, DataType):
            return False

        # Verify it is a Dict by checking the attribute
        # dict_types is present
        if not hasattr(other, 'dict_dtypes'):
            return False

        # Check if every key in the defined class is present
        # in the other instance.
        # And check if the values for a given key coincide in both.
        for key in self.dict_dtypes:
            if key not in other.dict_dtypes:
                return False
            self_dtype = self.dict_dtypes[key]
            other_dtype = other.dict_dtypes[key]
            if not self_dtype == other_dtype:
                return False

        # Check if there are no additional keys in other instance
        for other_key in other.dict_dtypes:
            if other_key not in self.dict_dtypes:
                return False

        return True

    def __repr__(self):
        dictionary = {
            key: repr(value)
            for key, value in self.dict_dtypes.items()
        }
        return 'Dict({})'.format(repr(dictionary))

    def __str__(self):
        dictionary = {
            key: str(value)
            for key, value in self.dict_dtypes.items()
        }
        return str(dictionary)


class List(DataType):
    """
    List DataType.

    The List DataType can have any size, but is restricted to a single
    DataType in all its entries. This DataType should be given in
    initialization. Example: List(Int())
    """

    def __init__(self, dtype):
        """Create a List DataType from a DataType."""
        # Check that given dtype is a valid DataType
        if not isinstance(dtype, DataType):
            message = 'Given dtype is not a DataType. (type={})'
            message = message.format(type(dtype))
            raise ValueError(message)
        self.list_item_type = dtype

    def validate(self, other):
        """Check if argument is a Tuple of this type."""
        # Verify other is tuple or list
        if not isinstance(other, (tuple, list)):
            return False

        # Verify all entries have the corresponding DataType
        for item in other:
            if not self.list_item_type.validate(item):
                return False

        return True

    def __eq__(self, other):
        if not isinstance(other, DataType):
            return False

        # Verify it is a list from attribute list_item_type
        if not hasattr(other, 'list_item_type'):
            return False

        # Compare list_item_type DataTypes from both Lists
        return self.list_item_type == other.list_item_type

    def __repr__(self):
        return 'List({})'.format(repr(self.list_item_type))

    def __str__(self):
        return 'List[{}]'.format(str(self.list_item_type))


class String(DataType):
    """
    String DataType.

    For simple types such as String, Int, Bool, and Float, the validate
    function verifies type is the corresponding type in python. No aditional
    parameters are needed for initialization.
    Example: String()
    """

    def validate(self, other):
        """Check if argument is a String."""
        return isinstance(other, str)

    def __repr__(self):
        return 'String()'

    def __str__(self):
        return 'String'


class Int(DataType):
    """Integer DataType."""

    def validate(self, other):
        """Check if argument is an Int."""
        return isinstance(other, int)

    def __repr__(self):
        return 'Int()'

    def __str__(self):
        return 'Int'


class Bool(DataType):
    """Boolean DataType."""

    def validate(self, other):
        """Check if argument is a Boolean."""
        return isinstance(other, bool)

    def __repr__(self):
        return 'Bool()'

    def __str__(self):
        return 'Bool'


class Float(DataType):
    """Floating number DataType."""

    def validate(self, other):
        """Check if argument is a Float."""
        return isinstance(other, float)

    def __repr__(self):
        return 'Float()'

    def __str__(self):
        return 'Float'
    
# Implementar Numpy Array
class NumpyArray(DataType):
    def __init__(self, dtype, shape):
        if not isinstance(dtype, DataType):
            message = 'Given dtype is not a DataType. (type={})'
            message = message.format(type(dtype))
            raise ValueError(message)
        if not isinstance(shape, tuple):
            message = 'Given shape should be given as a tuple. (type={})'
            message = message.format(type(dtype))
            raise ValueError(message)
        for item in shape:
            if not isinstance(item, int):
                message = 'All entries of shape should be of type int. (type={})'
                message = message.format(type(dtype))
                raise ValueError(message)
        self.nparray_item_type = dtype
        self.shape=shape
        
    def validate(self, other):
       if not (isinstance(other, np.ndarray)):
           print("Not np.array")
           return False
       if not (self.shape==other.shape):
           print("bad shape")
           return False
       aux=other.reshape(np.prod(other.shape))
       for item in aux:
           if not (self.nparray_item_type.validate(item)):
               print("bad type")
               return False
       return True
   
    def __eq__(self, other):
        if not (isinstance(other, np.ndarray)):
           return False
        if not (self.nparray_item_type==other.dtype):
           return False
        if not (self.shape==other.shape):
           return False
        return True
        
