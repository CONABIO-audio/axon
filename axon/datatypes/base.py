from abc import ABC
from abc import abstractmethod


def Tuple(array):
    for dtype in array:
        if not issubclass(dtype, DataType):
            message = 'Array value is not a DataType. (type={})'
            message = message.format(type(value))
            raise ValueError(message)

    class TupleType(DataType):
        tuple_data_types = array

        @classmethod
        def validate(cls, other):
            if not isinstance(other, (tuple, list)):
                return False

            if len(other) != len(array):
                return False

            for other_item, array_dtype in zip(other, array):
                if not array_dtype.validate(other_item):
                    return False

            return True

        @classmethod
        def eq(cls, other):
            if not issubclass(other, DataType):
                return False

            if not hasattr(other, 'tuple_data_types'):
                return False

            if len(cls.tuple_data_types) != len(other.tuple_data_types):
                return False

            for cls_dtype, other_dtype in zip(cls.tuple_data_types,
                    other.tuple_data_types):
                if not cls_dtype.eq(other_dtype):
                    return False

            return True

    return TupleType


def Dict(types):
    for value in types.values():
        if not issubclass(value, DataType):
            message = 'Dictionary value is not a DataType. (type={})'
            message = message.format(type(value))
            raise ValueError(message)

    class DictType(DataType):
        dict_dtypes = types

        @classmethod
        def validate(cls, other):
            if not isinstance(other, dict):
                return False

            for key, value in types.items():
                if key not in other:
                    return False

                if not value.validate(other[key]):
                    return False

            return True

        @classmethod
        def eq(cls, other):
            if not issubclass(other, DataType):
                return False

            if not hasattr(other, 'dict_dtypes'):
                return False

            for key in cls.dict_dtypes:
                if not key in other.dict_dtypes:
                    return False

                cls_dtype = cls.dict_dtypes[key]
                other_dtype = other.dict_dtypes[key]
                if not cls_dtype.eq(other_dtype):
                    return False

            for other_key in other.dict_dtypes:
                if other_key not in cls.dict_dtypes:
                    return False

            return True

    return DictType


def List(dtype):
    return dtype.list()


class DataType(ABC):
    @classmethod
    @abstractmethod
    def validate(cls, other):
        pass

    @classmethod
    def eq(cls, other):
        return other == cls

    @classmethod
    def list(cls):
        class ListType(DataType):
            list_item_type = cls

            @classmethod
            def validate(new_cls, other):
                if not isinstance(other, (tuple, list)):
                    return False

                for item in other:
                    if not cls.validate(item):
                        return False

                return True

            @classmethod
            def eq(cls, other):
                if not issubclass(other, DataType):
                    return False

                if not hasattr(other, 'list_item_type'):
                    return False

                return cls.list_item_type == other.list_item_type

        return ListType


class String(DataType):
    @classmethod
    def validate(cls, other):
        return isinstance(other, str)

    def __repr__(self):
        return 'String'

    def __str__(self):
        return 'String'


class Int(DataType):
    @classmethod
    def validate(cls, other):
        return isinstance(other, int)


class Bool(DataType):
    @classmethod
    def validate(cls, other):
        return isinstance(other, bool)


class Float(DataType):
    @classmethod
    def validate(cls, other):
        return isinstance(other, float)


# TODO: Implementar Numpy Array
# TODO: Implementar DataFrame
