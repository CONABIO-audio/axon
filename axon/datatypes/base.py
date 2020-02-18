from abc import ABC
from abc import abstractmethod


def Tuple(array):
    for dtype in array:
        if not isinstance(dtype, DataType):
            message = 'Array value is not a DataType. (type={})'
            message = message.format(type(value))
            raise ValueError(message)

    class TupleType(DataType):
        tuple_data_types = array

        def validate(cls, other):
            if not isinstance(other, (tuple, list)):
                return False

            if len(other) != len(array):
                return False

            for other_item, array_dtype in zip(other, array):
                if not array_dtype.validate(other_item):
                    return False

            return True

        def __eq__(self, other):
            if not isinstance(other, DataType):
                return False

            if not hasattr(other, 'tuple_data_types'):
                return False

            if len(self.tuple_data_types) != len(other.tuple_data_types):
                return False

            for self_dtype, other_dtype in zip(self.tuple_data_types,
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

    return TupleType()


def Dict(types):
    for value in types.values():
        if not isinstance(value, DataType):
            message = 'Dictionary value is not a DataType. (type={})'
            message = message.format(type(value))
            raise ValueError(message)

    class DictType(DataType):
        dict_dtypes = types

        def validate(self, other):
            if not isinstance(other, dict):
                return False

            for key, value in types.items():
                if key not in other:
                    return False

                if not value.validate(other[key]):
                    return False

            return True

        def __eq__(self, other):
            if not isinstance(other, DataType):
                return False

            if not hasattr(other, 'dict_dtypes'):
                return False

            for key in self.dict_dtypes:
                if not key in other.dict_dtypes:
                    return False

                self_dtype = self.dict_dtypes[key]
                other_dtype = other.dict_dtypes[key]
                if not self_dtype==other_dtype:
                    return False

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

    return DictType()


def List(dtype):
    class ListType(DataType):
        list_item_type = dtype
        def validate(self, other):
            if not isinstance(other, (tuple, list)):
                return False
            for item in other:
                if not self.list_item_type.validate(item):
                    return False

            return True

        def __eq__(self, other):
            if not isinstance(other, DataType):
                return False

            if not hasattr(other, 'list_item_type'):
                return False

            return self.list_item_type == other.list_item_type

        def __repr__(self):
            return 'List({})'.format(repr(self.list_item_type))

        def __str__(self):
            return 'List[{}]'.format(str(self.list_item_type))

    return ListType()


class DataType(ABC):
    @abstractmethod
    def validate(self, other):
        pass

    def __eq__(self, other):
        return(type(self)==type(other))

     


class String(DataType):
    def validate(self, other):
        return isinstance(other, str)

    def __repr__(self):
        return 'String()'

    def __str__(self):
        return 'String'


class Int(DataType):
    def validate(self, other):
        return isinstance(other, int)

    def __repr__(self):
        return 'Int()'

    def __str__(self):
        return 'Int'


class Bool(DataType):
    def validate(self, other):
        return isinstance(other, bool)

    def __repr__(self):
        return 'Bool()'

    def __str__(self):
        return 'Bool'


class Float(DataType):
    def validate(self, other):
        return isinstance(other, float)

    def __repr__(self):
        return 'Float()'

    def __str__(self):
        return 'Float'

# TODO: Implementar Numpy Array
# TODO: Implementar DataFrame
