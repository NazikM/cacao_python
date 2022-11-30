from abc import ABC, abstractmethod
from decimal import Decimal as DecimalNumber, getcontext, InvalidOperation
from datetime import datetime

MISSING = object()


class Schema:
    def __init__(self, **kwargs):
        for key, value in type(self).__dict__.items():
            if isinstance(value, Field):
                try:
                    setattr(self, key, kwargs.get(key, MISSING))
                except TypeError:
                    raise TypeError(f"Missing a required value for field {key}")

    def to_dict(self):
        res = {}
        for key, value in type(self).__dict__.items():
            if isinstance(value, NestedField):
                res[key] = getattr(self, key).to_dict()
            elif isinstance(value, Field) and not value.write_only:
                res[key] = getattr(self, key)
        return res


class Field(ABC):
    def __init__(self, required=True, default=MISSING, write_only=False):
        if not required and default is not MISSING:
            raise TypeError(f"You cannot specify required=False with default argument. Try to put  required=True")

        self.required = required
        self.default = default
        self.write_only = write_only

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        if self.write_only:
            raise AttributeError("This is write only attribute")
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        if self.required and (value is MISSING) and (self.default is MISSING):
            raise TypeError(f"Missing a required value for field with type {self}")

        if value is MISSING:
            if self.default is MISSING:
                value = None
            else:
                value = self.default

        if value:
            self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class IntegerField(Field):
    def __init__(self, min_value=None, max_value=None, **kwargs):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        try:
            value = int(value)
        except TypeError:
            raise TypeError(f"Expected integer value, but given {type(value)}") from None
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Expected value less than {self.min_value}, but given {value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Expected value bigger than {self.max_value}, but given {value}")

    def __str__(self):
        return "Integer"

    def __set__(self, obj, value):
        super().__set__(obj, value)
        setattr(obj, self.private_name, int(value))


class StringField(Field):
    def __init__(self, min_length=None, max_length=None, strict=True, **kwargs):
        super().__init__(**kwargs)
        self.min_length = min_length
        self.max_length = max_length
        self.strict = strict

    def validate(self, value):
        if self.strict and not isinstance(value, str):
            raise TypeError(f"Expected string value, but given {type(value)}") from None

        value = str(value)
        if self.min_length is not None and len(value) < self.min_length:
            raise ValueError(f"Expected length less than {self.min_length}")
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(f"Expected length bigger than {self.max_length}")

    def __str__(self):
        return "String"


class DecimalField(Field):
    def __init__(self, min_value=None, max_value=None, as_float=False, precision=12, **kwargs):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.as_float = as_float
        self.precision = precision

    def validate(self, value):
        try:
            if self.as_float:
                value = float(value)
            else:
                getcontext().prec = self.precision
                value = DecimalNumber(value)
        except (TypeError, InvalidOperation):
            raise TypeError(f"Expected Decimal value, but given {type(value)}") from None
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Expected value less than {self.min_value}, but given {value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Expected value bigger than {self.max_value}, but given {value}")

    def __set__(self, obj, value):
        super().__set__(obj, value)
        setattr(obj, self.private_name, float(value) if self.as_float else DecimalNumber(value))

    def __str__(self):
        return "Decimal"


class DateTimeField(Field):
    def validate(self, value):
        if isinstance(value, datetime) and not isinstance(value, str):
            raise TypeError(f"Expected string or datetime type, but given {type(value)}") from None

    def __str__(self):
        return "Datetime"


class NestedField(Field):
    def __init__(self, schema=None, **kwargs):
        super().__init__(**kwargs)
        self.schema = schema

    def validate(self, value):
        # print(self.schema.__mro__, Schema, isinstance(self.schema, Schema))
        # Why is not working ???
        # if not isinstance(self.schema, Schema):
        if Schema not in self.schema.__mro__:
            raise TypeError(f"Expected Schema type, but given {type(value)}") from None
