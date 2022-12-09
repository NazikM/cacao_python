from cacao.src.cacao.cacao import classes


class Marks(classes.Schema):
    mark_1 = classes.IntegerField(min_value=0, max_value=100)
    mark_2 = classes.IntegerField(min_value=0, max_value=100)


class Test(classes.Schema):
    full_name = classes.StringField(max_length=200)
    age = classes.IntegerField(default=21, min_value=18, max_value=21)
    money = classes.DecimalField(write_only=True)
    marks = classes.NestedField(Marks)


marks = Marks(mark_1=86, mark_2=98)
t = Test(full_name="Nazarii Marusyn", age='20', money='23.4564566', marks={"mark_1": 86, "mark_2": 98})

print(t.to_dict())

data = {
    "full_name": "Nazarii Marusyn",
    "age": '20',
    'money': "23.34534",
    "marks": {
        "mark_1": 86,
        "mark_2": 98
    }
}
t2 = Test.from_dict(data).to_dict()
print(t2)


