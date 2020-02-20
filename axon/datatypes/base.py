# -*- coding: utf-8 -*-
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


class DataType(ABC):
    """
    The Datatype base class.

    Has the validate and __eq__ methods. Since validate
    is an abstract method it must be redefined for every data type accordingly.
    """

    def __init__(self, description=None):
        """Create a DataType."""
        self.description = description

    @abstractmethod
    def validate(self, other):
        """Check if object is of this datatype."""

    def __eq__(self, other):
        """Check if two datatypes are the same."""
        return isinstance(other, type(self))

    def __ne__(self, other):
        """Check if other is not the same DataType."""
        return not self.__eq__(other)

    def __or__(self, other):
        """Return the conjunction of the two data types."""
        return ConjunctionDataType(self, other)

    def __ror__(self, other):
        """Return the conjunction of the two data types."""
        return ConjunctionDataType(other, self)


class ConjunctionDataType(DataType):
    """
    Conjunction DataType.

    Represents a datum which can be one of two different datatypes.
    """

    def __init__(self, first, second, **kwargs):
        """Create a conjunction datatype."""
        if not isinstance(first, DataType):
            message = "{} is not a DataType instance".format(first)
            raise ValueError(message)

        if not isinstance(second, DataType):
            message = "{} is not a DataType instance".format(second)
            raise ValueError(message)

        super().__init__(**kwargs)
        self.first = first
        self.second = second

    def validate(self, other):
        """Check if is one of the two declared datatypes."""
        if self.first.validate(other):
            return True

        return self.second.validate(other)

    def __eq__(self, other):
        """Check if is the same DataType as other."""
        if not isinstance(other, ConjunctionDataType):
            return False

        if (self.first == other.first) and (self.second == other.second):
            return True

        return (self.first == other.second) and (self.second == other.first)

    def __ne__(self, other):
        """Check if other is not the same DataType."""
        return not self.__eq__(other)

    def __repr__(self):
        """Get full representation."""
        return '{} | {}'.format(repr(self.first), repr(self.second))


class Tuple(tuple, DataType):
    """
    The Tuple DataType.

    The tuple datatype is an array of a fixed length and every entry may be
    a different Datatype.
    To initialize a Tuple an array with the DataTypes of each entry must be
    given.

    Example: Tuple([Int(), Bool(), String()])
    """

    def __new__(cls, type_array, **kwargs):
        """Create a Tuple from list of datatypes."""
        # pylint: disable=unused-argument
        if not isinstance(type_array, (tuple, list)):
            message = 'Tuple argument is not tuple/list. (arg={})'
            message = message.format(type_array)
            raise ValueError(message)

        # Verify if the entries correspond to an accepted DataType
        for dtype in type_array:
            if not isinstance(dtype, DataType):
                message = 'Array value is not a DataType. (type={})'
                message = message.format(type(dtype))
                raise ValueError(message)

        return tuple.__new__(cls, type_array)

    def __init__(self, type_array, **kwargs):
        """Create a Tuple from list of datatypes."""
        # pylint: disable=unused-argument,super-init-not-called
        DataType.__init__(self, **kwargs)

    def validate(self, other):
        """Check if argument is a Tuple."""
        # Verify if other is a tuple or list
        if not isinstance(other, (tuple, list)):
            return False

        # Check if length of the defined tuple coincides with other's length
        if len(other) != len(self):
            return False

        # Verify that the datatypes coincide in each entry
        for other_item, array_dtype in zip(other, self):
            if not array_dtype.validate(other_item):
                return False

        return True

    def __eq__(self, other):
        """Check if is the same DataType as other."""
        # Check DataType is valid
        if not isinstance(other, DataType):
            return False

        # Verify it is a tuple
        if not isinstance(other, tuple):
            return False

        # Check if lengths coincide
        if len(self) != len(other):
            return False

        # Verify that the datatypes coincide in each entry
        for self_dtype, other_dtype in zip(self, other):
            if not self_dtype == other_dtype:
                return False

        return True

    def __ne__(self, other):
        """Check if other is not the same DataType."""
        return not self.__eq__(other)

    def __repr__(self):
        """Get full representation."""
        reprs = tuple([repr(dtype) for dtype in self])
        return 'Tuple({})'.format(repr(reprs))

    def __str__(self):
        """Get string representation."""
        str_tuple = tuple([str(dtype) for dtype in self])
        return str(str_tuple)


class Dict(dict, DataType):
    """
    Dictionary Datatype.

    To define a Dict one must include the structure of the dictionary with
    its corresponding keys and DataType for each key.
    Example: Dict({'Key1':Int(), 'Key2':Bool()})
    """

    def __new__(cls, dtypes_dict, **kwargs):
        """Create a Dict DataType from dictionary of DataTypes."""
        # pylint: disable=unused-argument
        # Verify dtypes_dict is a dictionary
        if not isinstance(dtypes_dict, dict):
            message = "Argument for Dict is not a dictionary. (arg={})"
            message = message.format(dtypes_dict)
            raise ValueError(message)

        # Verify the DataTypes for the values are valid DataTypes.
        for value in dtypes_dict.values():
            if not isinstance(value, DataType):
                message = 'Dictionary value is not a DataType. (type={})'
                message = message.format(type(value))
                raise ValueError(message)

        return super(Dict, cls).__new__(cls, dtypes_dict)

    def __init__(self, dtypes_dict, **kwargs):
        """Create a Dict DataType from dictionary of DataTypes."""
        dict.__init__(self, dtypes_dict)
        DataType.__init__(self, **kwargs)

    def validate(self, other):
        """Check if argument is of this Dict type."""
        if not isinstance(other, dict):
            return False

        # Check if every key in the defined class is present
        # in the other instance.
        # And check if the values for a given key coincide in both.
        for key, value in self.items():
            if key not in other:
                return False
            if not value.validate(other[key]):
                return False

        # Check if there are keys in instance that are not
        # in the defined dtype
        for key in other:
            if key not in self:
                return False

        return True

    def __eq__(self, other):
        """Check if is the same DataType as other."""
        # Check if it is a valid DataType
        if not isinstance(other, DataType):
            return False

        # Verify it is a dict
        if not isinstance(other, dict):
            return False

        # Check if every key in the defined class is present
        # in the other instance.
        # And check if the values for a given key coincide in both.
        for key in self:
            if key not in other:
                return False
            self_dtype = self[key]
            other_dtype = other[key]
            if not self_dtype == other_dtype:
                return False

        # Check if there are no additional keys in other instance
        for other_key in other:
            if other_key not in self:
                return False

        return True

    def __ne__(self, other):
        """Check if other is not the same DataType."""
        return not self.__eq__(other)

    def __repr__(self):
        """Get full representation."""
        return 'Dict({})'.format(dict.__repr__(self))

    def __str__(self):
        """Get string representation."""
        str_dict = {
            key: str(value)
            for key, value in self.items()
        }
        return str(str_dict)


class List(DataType):
    """
    List DataType.

    The List DataType can have any size, but is restricted to a single
    DataType in all its entries. This DataType should be given in
    initialization. Example: List(Int())
    """

    def __init__(self, dtype, **kwargs):
        """Create a List DataType from a DataType."""
        super().__init__(**kwargs)

        # Check that given dtype is a valid DataType
        if not isinstance(dtype, DataType):
            print(dtype)
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
        """Check if is the same DataType as other."""
        if not isinstance(other, DataType):
            return False

        # Verify it is a list from attribute list_item_type
        if not hasattr(other, 'list_item_type'):
            return False

        # Compare list_item_type DataTypes from both Lists
        return self.list_item_type == other.list_item_type

    def __ne__(self, other):
        """Check if other is not the same DataType."""
        return not self.__eq__(other)

    def __repr__(self):
        """Get full representation."""
        return 'List({})'.format(repr(self.list_item_type))

    def __str__(self):
        """Get string representation."""
        return '[{}, ...]'.format(str(self.list_item_type))


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
        """Get full representation."""
        if self.description:
            return 'String(description="{}")'.format(self.description)

        return 'String()'

    def __str__(self):
        """Get string representation."""
        if self.description:
            return '{} (str)'.format(self.description)

        return 'str'


class Int(DataType):
    """Integer DataType."""

    def validate(self, other):
        """Check if argument is an Int."""
        return isinstance(other, int)

    def __repr__(self):
        """Get full representation."""
        if self.description:
            return 'Int(description="{}")'.format(self.description)

        return 'Int()'

    def __str__(self):
        """Get string representation."""
        if self.description:
            return '{} (int)'.format(self.description)

        return 'int'


class Bool(DataType):
    """Boolean DataType."""

    def validate(self, other):
        """Check if argument is a Boolean."""
        return isinstance(other, bool)

    def __repr__(self):
        """Get full representation."""
        if self.description:
            return 'Bool(description="{}")'.format(self.description)

        return 'Bool()'

    def __str__(self):
        """Get string representation."""
        if self.description:
            return '{} (bool)'.format(self.description)

        return 'bool'


class Float(DataType):
    """Floating number DataType."""

    def validate(self, other):
        """Check if argument is a Float."""
        return isinstance(other, float)

    def __repr__(self):
        """Get full representation."""
        if self.description:
            return 'Float(description="{}")'.format(self.description)

        return 'Float()'

    def __str__(self):
        """Get string representation."""
        if self.description:
            return '{} (float)'.format(self.description)

        return 'float'


class NoneType(DataType):
    """None DataType."""

    def validate(self, other):
        """Check if argument is None."""
        return other is None

    def __repr__(self):
        """Get full representation."""
        return 'NoneType()'

    def __str__(self):
        """Get string representation."""
        return 'None'
