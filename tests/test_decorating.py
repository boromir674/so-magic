import pytest


@pytest.fixture
def test_infra():
    from so_magic.data.backend.backend import MyDecorator, CommandRegistrator
    return type('TestInfra', (object,), dict(MyDecorator=MyDecorator, CommandRegistrator=CommandRegistrator))


def test_type_class_properties(test_infra):
    assert not hasattr(test_infra.CommandRegistrator, 'registry')
    assert not hasattr(test_infra.CommandRegistrator, 'state')
    assert not hasattr(test_infra.MyDecorator, '_commands_hash')


@pytest.fixture
def test_objects(test_infra):
    class A(test_infra.MyDecorator): pass
    class Ab(test_infra.MyDecorator): pass
    class B(metaclass=test_infra.MyDecorator): pass
    DynamicClass = test_infra.MyDecorator('DynamicClass', (object,), {})
    class ParentClass: pass
    class DefinedClass(ParentClass, metaclass=test_infra.MyDecorator): pass
    inst1 = DynamicClass()
    inst2 = DefinedClass()
    inst3 = B()
    return type('TestObjects', (object,), {
        'type_classes': type('TypeClasses', (object,), {'A': A, 'Ab': Ab, '__iter__': lambda self: iter([A, Ab])})(),
        'normal_classes': type('NormalClasses', (object,), {'B': B, 'DynamicClass': DynamicClass, 'DefinedClass': DefinedClass, '__iter__': lambda self: iter([B, DynamicClass, DefinedClass])})(),
        'instances': type('Instances', (object,), {'DynamicClass': inst1, 'DefinedClass': inst2, 'B': inst3, '__iter__': lambda self: iter([inst1, inst2, inst3])}),
        'MyDecorator': test_infra.MyDecorator,
        'have_magic_decorator': [type(type(inst1)), type(DynamicClass), test_infra.MyDecorator, A, Ab, B, DynamicClass,
                                 DefinedClass]
    })


def test_decorating(test_objects):
    assert all(type(x) == type for x in (test_objects.MyDecorator, test_objects.type_classes.A))
    assert all(type(x) == test_objects.MyDecorator
               for x in (test_objects.normal_classes.B, test_objects.normal_classes.DynamicClass))
    assert all(type(getattr(test_objects.instances, x)) == getattr(test_objects.normal_classes, x) for x in ('DynamicClass', 'DefinedClass', 'B'))
    assert not hasattr(test_objects.instances.B, 'magic_decorator')
    assert not hasattr(test_objects.instances.DefinedClass, 'magic_decorator')
    assert all([hasattr(x, 'magic_decorator') for x in test_objects.have_magic_decorator])
    assert id(test_objects.type_classes.A.magic_decorator) != id(test_objects.type_classes.Ab.magic_decorator)
    assert len(set([id(o.magic_decorator) for o in test_objects.have_magic_decorator])) == 1


@pytest.fixture
def classes(test_infra):
    class ADecoratorClass(metaclass=test_infra.CommandRegistrator): pass
    class BDecoratorClass(metaclass=test_infra.CommandRegistrator): pass

    @ADecoratorClass.func_decorator()
    def aa(x):
        return str(x) + 'aa'

    @BDecoratorClass.func_decorator()
    def bb(x):
        return str(x) + 'bb'
    value = 1
    return [{'c': c, 'test_data': (value, f'{value}{decorated_func_name}')}
            for c, decorated_func_name in zip([ADecoratorClass, BDecoratorClass], ['aa', 'bb'])]


def test_decorator(classes):
    func_names = ('aa', 'bb')
    assert all(func_name in test_data['c'].registry for func_name, test_data in zip(func_names, classes))
    assert all(func_name not in test_data['c'].registry for func_name, test_data in zip(func_names, reversed(classes)))
    assert all(test_data['c'].registry[func_name](test_data['test_data'][0]) == test_data['test_data'][1]
               for func_name, test_data in zip(func_names, classes))
