from cacao.src.cacao.cacao import fields, schemas


class Marks(schemas.Schema):
    mark_1 = fields.IntegerField(min_value=0, max_value=100)
    mark_2 = fields.IntegerField(min_value=0, max_value=100)


class Test(schemas.Schema):
    full_name = fields.StringField(max_length=200)
    age = fields.IntegerField(default=21, min_value=18, max_value=27)
    money = fields.DecimalField(write_only=True)
    marks = fields.NestedField(Marks)
    rich = fields.MethodField()

    def get_rich(self):
        return True if self.money > 26 else False


marks = Marks(mark_1=86, mark_2=98)
t = Test(full_name="Nazarii Marusyn", age='20', money='27.4564566', marks={"mark_1": 86, "mark_2": 98})
t.age = 19
print(t.to_dict())

data = {
    "full_name": "Nazarii Marusyn",
    'age': 21,
    'money': "33.34534",
    "marks": {
        "mark_1": 86,
        "mark_2": 98
    }
}
t2 = Test.from_dict(data)
print(t2.to_dict())


class TestSchema(schemas.Schema):
    name = fields.StringField(max_length=100)
    nested_schema = fields.NestedField('self')


# data2 = {
#     'name': 't',
#     'nested_schema': {
#         'name': 'world'
#     }
# }
#
# print(TestSchema.from_dict(data2).to_dict())
