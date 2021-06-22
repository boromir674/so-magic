import pytest


@pytest.fixture
def test_infra():
    from so_magic.data.backend.backend import MyDecorator, CommandRegistrator
    return type('TestInfra', (object,), dict(MyDecorator=MyDecorator, CommandRegistrator=CommandRegistrator))


def test_type_class_properties(test_infra):
    assert not hasattr(test_infra.CommandRegistrator, 'registry')
    assert not hasattr(test_infra.CommandRegistrator, 'state')
    assert not hasattr(test_infra.MyDecorator, '_commands_hash')


def test_decorating(test_infra):
    class A(test_infra.MyDecorator): pass
    class Ab(test_infra.MyDecorator): pass
    class B(metaclass=test_infra.MyDecorator): pass

    assert type(test_infra.MyDecorator) == type
    assert type(A) == type
    assert type(B) == test_infra.MyDecorator

    DynamicClass = test_infra.MyDecorator('DynamicClass', (object,), {})
    assert type(DynamicClass) == test_infra.MyDecorator
    o1 = DynamicClass()
    assert type(o1) == DynamicClass

    class ParentClass: pass
    class DefinedClass(ParentClass, metaclass=test_infra.MyDecorator): pass
    dc = DefinedClass()
    assert type(dc) == DefinedClass

    b = B()
    assert type(b) == B

    objects = (test_infra.MyDecorator, A, Ab, B, type(DynamicClass), type(type(o1)), DefinedClass)
    assert all([hasattr(x, 'magic_decorator') for x in objects])

    assert id(A.magic_decorator) != id(Ab.magic_decorator)
    assert len(set([id(o.magic_decorator) for o in objects])) == 1


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
