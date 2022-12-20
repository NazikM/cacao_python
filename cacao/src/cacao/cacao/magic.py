from cacao.src.cacao.cacao.fields import Field
from cacao.src.cacao.cacao.missing import MISSING

init_template = "def __init__({arguments}):\n\t{assignments}"


def autoinit(klass=None, merge=False):
    def inner(cls):
        arguments = ["self"]
        assignments = []
        namespace = {'MISSING': MISSING}

        for key, value in vars(cls).items():
            if isinstance(value, Field):
                arguments.append(f'{key}=MISSING')
                assignments.append(f'self.{key} = {key}')

        if merge:
            arguments.extend(('*args', '**kwargs'))
            assignments.append(f'user_default_init(self, *args, **kwargs)')
            namespace['user_default_init'] = cls.__init__

        init = init_template.format(
            arguments=', '.join(arguments),
            assignments='\n\t'.join(assignments)
        )
        exec(init, namespace)
        cls.__init__ = namespace['__init__']
        return cls
    if klass is not None:
        return inner(klass)
    return inner
