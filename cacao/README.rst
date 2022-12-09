Cacao
===============
small validator and serializer for your needs. To start using that please follow the instructions bellow.

Installing
============

.. code-block:: bash

    pip install multi-cacao

Usage
=====

.. code-block:: python

    >>> from cacao.cacao import classes
    >>>
    >>> class Marks(classes.Schema):
    >>>     mark_1 = classes.IntegerField(min_value=0, max_value=100)
    >>>     mark_2 = classes.IntegerField(min_value=0, max_value=100)
    >>>
    >>> class Test(classes.Schema):
    >>>     full_name = classes.StringField(max_length=200)
    >>>     age = classes.IntegerField(default=21, min_value=18, max_value=21)
    >>>     money = classes.DecimalField(write_only=True)
    >>>     marks = classes.NestedField(Marks)
    >>>     marks = Marks(mark_1=86, mark_2=98)
    >>>     t = Test(full_name="Nazarii Marusyn", age='20', money='23.4564566', marks={"mark_1": 86, "mark_2": 98})
    >>>     
    >>>     print(t.to_dict()) -> {'full_name': 'Nazarii Marusyn', 'age': 20, 'marks': {'mark_1': 86, 'mark_2': 98}}
    >>>     
    >>>     data = {
    >>>         "full_name": "Nazarii Marusyn",
    >>>         "age": '20',
    >>>         'money': "23.34534",
    >>>         "marks": {
    >>>             "mark_1": 86,
    >>>             "mark_2": 98
    >>>         }
    >>>     }
    >>>     t2 = Test.from_dict(data).to_dict()
    >>>     print(t2) -> {'full_name': 'Nazarii Marusyn', 'age': 20, 'marks': {'mark_1': 86, 'mark_2': 98}}

As you see firstly we should create Schemas that inherite from Schema abstractclass.

After that you have choice how to fill data into schema:

1) Just put as kwargs params.

>>> Test(full_name="Nazarii Marusyn", age='20', money='23.4564566', marks={"mark_1": 86, "mark_2": 98})

2) Call method from_dict and pass there your dictionary params.

>>>     data = {
>>>         "full_name": "Nazarii Marusyn",
>>>         "age": '20',
>>>         'money': "23.34534",
>>>         "marks": {
>>>             "mark_1": 86,
>>>             "mark_2": 98
>>>         }
>>>     }
>>>     t2 = Test.from_dict(data)

Here t1 == t2.
 
