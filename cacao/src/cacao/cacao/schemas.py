from cacao.src.cacao.cacao.fields import Field
from cacao.src.cacao.cacao.missing import MISSING

# __all__ = (
#     'Schema',
#     'MISSING',
#     # 'Field',
#     # 'IntegerField',
#     # 'StringField',
#     # 'DecimalField',
#     # 'DateTimeField',
#     # 'NestedField'
# )


class OnlyFieldsMeta(type):
    def __new__(cls, clsname, bases, attrs):
        for name, val in attrs.items():
            if name not in ('__module__', '__qualname__'):
                if not isinstance(val, (Field, classmethod)) and not callable(val):
                    raise ValueError("You cannot create not Field attributes inside the Schema")
        return type(clsname, bases, attrs)


class Schema(metaclass=OnlyFieldsMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key not in vars(type(self)):
                raise TypeError("Too many arguments!")

        for key, value in vars(type(self)).items():
            if isinstance(value, Field):
                setattr(self, key, kwargs.get(key, MISSING))

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_dict(self):
        res = {}
        for key, value in type(self).__dict__.items():
            if isinstance(value, Field) and not value.write_only:
                val = getattr(self, key)
                if val is not MISSING:
                    if isinstance(val, Schema):
                        val = val.to_dict()
                    res[key] = val
        return res

