from pathlib import Path
import os
from importlib.machinery import SourceFileLoader

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
            res = self.find_in_fields_files(key)
            if res:
                return res
            key, value = self.separate_key(key)
            func = Field.Fields[value]
            return wrapper

    def get_all_files_paths(self, path):
        res = []
        for i in os.listdir(path):
            if os.path.isdir(i):
                res += self.get_all_files_paths(os.path.join(path, i))
            elif i == "fields.py":
                res.append(os.path.join(path, i))
        return res

    def find_in_fields_files(self, key):
        root_dir = Path().absolute()
        for file_path in self.get_all_files_paths(root_dir):
            mod = SourceFileLoader("fields", file_path).load_module()
            if res := vars(mod).get(key):
                return res
        return None

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
