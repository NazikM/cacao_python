from cacao import cacao


class Marks(cacao.Schema):
    mark_1 = cacao.IntegerField(min_value=0, max_value=100)
    mark_2 = cacao.IntegerField(min_value=0, max_value=100)


class Test(cacao.Schema):
    full_name = cacao.StringField(max_length=200)
    age = cacao.IntegerField(default=21, min_value=18, max_value=21)
    money = cacao.DecimalField(write_only=True)
    marks = cacao.NestedField(Marks)


marks = Marks(mark_1=86, mark_2=98)
t = Test(full_name="Nazarii Marusyn", age='20', money='23.4564566', marks=marks)

print(t.to_dict())
