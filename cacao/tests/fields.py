from cacao.src.cacao.cacao import fields


class MyIntegerField(fields.IntegerField):
    def __get__(self, obj, obj_type=None):
        return super().__get__(obj, obj_type) + 100
