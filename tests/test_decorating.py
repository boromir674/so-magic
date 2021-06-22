import pytest


@pytest.fixture
def test_infra():
    from so_magic.data.backend.backend import MyDecorator, CommandRegistrator
    return type('TestInfra', (object,), dict(MyDecorator=MyDecorator, CommandRegistrator=CommandRegistrator))


def test_decorating(test_infra):
    assert not hasattr(test_infra.CommandRegistrator, 'registry')
    assert not hasattr(test_infra.CommandRegistrator, 'state')
    assert not hasattr(test_infra.MyDecorator, '_commands_hash')

    class A(test_infra.MyDecorator): pass
    class Ab(test_infra.MyDecorator): pass
    class B(metaclass=test_infra.MyDecorator): pass

    assert type(test_infra.MyDecorator) == type
    assert type(A) == type
    assert type(B) == test_infra.MyDecorator

    RuntimeClass = test_infra.MyDecorator('RuntimeClass', (object,), {})
    assert type(RuntimeClass) == test_infra.MyDecorator
    o1 = RuntimeClass()
    assert type(o1) == RuntimeClass

    RuntimeClassA = test_infra.MyDecorator('RuntimeClassA', (object,), {})
    assert type(RuntimeClassA) == test_infra.MyDecorator
    o2 = RuntimeClassA()
    assert type(o2) == RuntimeClassA

    class ParentClass: pass
    class DefinedClass(ParentClass, metaclass=test_infra.MyDecorator): pass
    dc = DefinedClass()
    assert type(dc) == DefinedClass

    b = B()
    assert type(b) == B

    objects = (test_infra.MyDecorator, A, Ab, B, type(RuntimeClass), type(type(o2)), DefinedClass)
    assert all([hasattr(x, 'magic_decorator') for x in objects])

    assert id(A.magic_decorator) != id(Ab.magic_decorator)
    assert len(set([id(o.magic_decorator) for o in objects])) == 1


def test_decorator(test_infra):
    class ADecoratorClass(metaclass=test_infra.CommandRegistrator): pass
    class BDecoratorClass(metaclass=test_infra.CommandRegistrator): pass

    @ADecoratorClass.func_decorator()
    def aa(x):
        return str(x) + 'aa'

    assert 'aa' in ADecoratorClass.registry
    assert 'aa' not in BDecoratorClass.registry
    assert ADecoratorClass.registry['aa']('1') == '1aa'

    @BDecoratorClass.func_decorator()
    def bb(x):
        return str(x) + 'bb'

    assert 'bb' in BDecoratorClass.registry
    assert 'bb' not in ADecoratorClass.registry
    assert BDecoratorClass.registry['bb']('1') == '1bb'
