
def test_decorating():
    from so_magic.data.command_factories import MyDecorator, CommandRegistrator


    class A(MyDecorator): pass
    class Ab(MyDecorator): pass
    class B(metaclass=MyDecorator): pass

    assert type(MyDecorator) == type
    assert type(A) == type
    assert type(B) == MyDecorator

    RuntimeClass = MyDecorator('RuntimeClass', (object,), {})
    assert type(RuntimeClass) == MyDecorator
    o1 = RuntimeClass()
    assert type(o1) == RuntimeClass

    RuntimeClassA = MyDecorator('RuntimeClassA', (object,), {})
    assert type(RuntimeClassA) == MyDecorator
    o2 = RuntimeClassA()
    assert type(o2) == RuntimeClassA

    class ParentClass: pass
    class DefinedClass(ParentClass, metaclass=MyDecorator): pass
    dc = DefinedClass()
    assert type(dc) == DefinedClass

    b = B()
    assert type(b) == B

    objects = (MyDecorator, A, Ab, B, type(RuntimeClass), type(type(o2)), DefinedClass)
    assert all([hasattr(x, 'magic_decorator') for x in objects])

    assert id(A.magic_decorator) != id(Ab.magic_decorator)
    assert len(set([id(o.magic_decorator) for o in objects])) == 1

    class ADecoratorClass(metaclass=CommandRegistrator): pass
    class BDecoratorClass(metaclass=CommandRegistrator): pass
    assert not hasattr(MyDecorator, '_commands_hash')
    assert not hasattr(CommandRegistrator, 'registry')
    assert not hasattr(CommandRegistrator, 'state')

    @ADecoratorClass.func_decorator()
    def aa():
        pass

    assert 'aa' in ADecoratorClass.registry
    assert 'aa' not in BDecoratorClass.registry

    @BDecoratorClass.func_decorator()
    def bb():
        pass

    assert 'bb' in BDecoratorClass.registry
    assert 'bb' not in ADecoratorClass.registry
