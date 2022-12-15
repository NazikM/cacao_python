from cacao.src.cacao.cacao import fields, schemas


# class MyIntegerField(fields.IntegerField):
#     def __get__(self, obj, obj_type=None):
#         return super().__get__(obj, obj_type) + 100


class Marks(schemas.Schema):
    mark_1 = MyIntegerField(min_value=0, max_value=200)
    mark_2IntegerField(min_value=0, max_value=200)

    def __post_init__(self, mark_1, mark_2):
        self.mark_1 = mark_1 + 5
        self.mark_2 = mark_2 + 10


marks2 = Marks(mark_1=6, mark_2=62)
print(marks2.to_dict())



# marks = Marks(mark_1=96, mark_2=98, mark=6)

# print(marks.to_dict())


# class Test(schemas.Schema):
#     full_name = fields.StringField(max_length=200)
#     age = fields.IntegerField(default=21, min_value=18, max_value=27)
#     money = fields.DecimalField(write_only=True)
#     marks = fields.NestedField(Marks)
#     rich = fields.MethodField()
#
#     def get_rich(self):
#         return True if self.money > 26 else False



# t = Test(full_name="Nazarii Marusyn", age='20', money='27.4564566', marks={"mark_1": 86, "mark_2": 98})
# t.age = 19
# print(t.to_dict())


# data = {
#     "full_name": "Nazarii Marusyn",
#     'age': 21,
#     'money': "33.34534",
#     "marks": {
#         "mark_1": 86,
#         "mark_2": 98
#     }
# }
# t2 = Test.from_dict(data)
# print(t2.to_dict())


class TestSchema(schemas.Schema):
    name = fields.StringField(max_length=100)
    nested_schema = fields.NestedField('self')


data2 = {
    'name': 'Hello',
    'nested_schema': {
        'name': 'world',
        'nested_schema': {
            'name': 'world'
        }
    }
}

# test2 = TestSchema.from_dict(data2)
# print(test2.to_dict())


# class Test2Schema(schemas.Schema):
#     full_name = fields.StringField(max_length=200)
#     testStringField(max_length=200)


# print(vars(Test2Schema))
