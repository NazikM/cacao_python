from cacao import cacao


class Test(cacao.Schema):
    full_name = cacao.String(max_length=200)
    age = cacao.Integer(default=21, min_value=18, max_value=21)
    money = cacao.Decimal(write_only=True)


t = Test(full_name="Nazarii Marusyn", age='20', money='23.4564566')

print(t.to_dict())

# import json
#
# with open('test.json') as f:
#     print(json.load(f))
#
# res = json.dumps({'test': 'jesff'}, indent=4)
# print(res)
