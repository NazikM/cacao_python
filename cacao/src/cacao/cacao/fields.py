from abc import ABC, abstractmethod
from decimal import Decimal as DecimalNumber, getcontext, InvalidOperation
from datetime import datetime

from cacao.src.cacao.cacao.missing import MISSING


class Field(ABC):
    def __init__(self, default=MISSING, write_only=False):
        self.default = default
        self.write_only = write_only

    def __set_name__(self, owner, name):
        self.field_name = name

    def __get__(self, obj, objtype=None):
        return self.value

    def __set__(self, obj, value):
        if value is MISSING:
            value = self.default
        else:
            self.validate(value)
            value = self.cast(obj, value)

        self.value = value

    @abstractmethod
    def validate(self, value):
        pass

    def cast(self, obj, value):
        return value


from cacao.src.cacao.cacao.schemas import Schema


class RequiredField(Field, ABC):
    def __init__(self, required=False, default=MISSING, write_only=False):
        super().__init__(default, write_only)

        if required and default is not MISSING:
            raise TypeError(f"'default' must not be set for required fields.")

        self.required = required

    def __set__(self, obj, value):
        if value is MISSING:
            if self.default is MISSING:
                self.raise_if_required()
            else:
                value = self.default
        else:
            self.validate(value)
            value = self.cast(obj, value)

        self.value = value

    def raise_if_required(self):
        if self.required:
            raise TypeError(f"Missing a required value for field {self.field_name}")


class MethodField(Field):
    def __init__(self, method=MISSING, **kwargs):
        super().__init__(**kwargs)
        self.method = method

    def get_name(self):
        if self.method is not MISSING:
            return self.method
        return "get_" + self.field_name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.get_name())()

    def validate(self, value):
        pass


class IntegerField(RequiredField):
    def __init__(self, min_value=None, max_value=None, **kwargs):
        super().__init__(**kwargs)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        try:
            value = int(value)
        except ValueError:
            raise ValueError(f"Expected integer value, but given '{value}'")

        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Expected value bigger than {self.min_value}, but given {value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Expected value less than {self.max_value}, but given {value}")

    def cast(self, obj, value):
        return int(value)


class StringField(RequiredField):
    def __init__(self, min_length=None, max_length=None, strict=True, **kwargs):
        super().__init__(**kwargs)
        self.min_length = min_length
        self.max_length = max_length
        self.strict = strict

    def validate(self, value):
        if self.strict and not isinstance(value, str):
            raise TypeError(f"Expected string value, but given {type(value)}")

        value = str(value)
        if self.min_length is not None and len(value) < self.min_length:
            raise ValueError(f"Expected length less than {self.min_length}")
        if self.max_length is not None and len(value) > self.max_length:
            raise ValueError(f"Expected length bigger than {self.max_length}")


class DecimalField(RequiredField):
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
            raise TypeError(f"Expected Decimal value, but given {type(value)}")
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Expected value less than {self.min_value}, but given {value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Expected value bigger than {self.max_value}, but given {value}")

    def cast(self, obj, value):
        return float(value) if self.as_float else DecimalNumber(value)


class DateTimeField(RequiredField):
    def validate(self, value):
        if isinstance(value, datetime) and not isinstance(value, str):
            raise TypeError(f"Expected string or datetime type, but given {type(value)}")


class NestedField(RequiredField):
    def __init__(self, schema, **kwargs):
        super().__init__(**kwargs)
        self.schema = schema

    def cast(self, obj, value):
        # if self.schema == 'self':
        #     self.schema = type(obj)
        return self.schema(**value)

    def validate(self, value):
        # if self.schema == 'self':
        #     return

        if not issubclass(self.schema, Schema):
            raise TypeError(f"Expected Schema type, but given {type(value)}")
