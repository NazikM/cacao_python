from cacao.src.cacao.cacao.fields import Field
from cacao.src.cacao.cacao.missing import MISSING


class Foo(dict):
    def __missing__(self, key):
        def wrapper(*args, **kwargs):
            self[key] = func(*args, **kwargs)
            return self[key]
        if not key.startswith('__'):
            if key == "classmethod" or key in Field.Fields or key == "fields":
                raise KeyError
            key, value = self.separate_key(key)
            func = Field.Fields[value]
            return wrapper

    def separate_key(self, key):
        for field_name in Field.Fields:
            if field_name in key:
                return key.replace(field_name, ''), field_name
        return key


class OnlyFieldsMeta(type):
    def __prepare__(self, *a):
        return Foo()

    def __new__(cls, clsname, bases, attrs):
        for name, val in attrs.items():
            if name not in ('__module__', '__qualname__'):
                if not isinstance(val, (Field, classmethod)) and not callable(val):
                    raise ValueError("You cannot create not Field attributes inside the Schema")
        return super().__new__(cls, clsname, bases, attrs)


class Schema(metaclass=OnlyFieldsMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in vars(type(self)):
                raise TypeError("Too many arguments!")

        self.__post_init__(**kwargs)

    def __post_init__(self, **kwargs):
        ...

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        res = {}
        for key, value in vars(type(self)).items():
            if isinstance(value, Field) and not value.write_only:
                val = getattr(self, key)
                if val is not MISSING:
                    if isinstance(val, Schema):
                        val = val.to_dict()
                    res[key] = val
        return res
