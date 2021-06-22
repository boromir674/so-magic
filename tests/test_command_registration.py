import pytest


@pytest.fixture
def modify_registry():
    def _modify_registry(registry, key, value):
        registry[key] = value
    return _modify_registry


@pytest.fixture
def classes():
    from so_magic.data.backend.backend import CommandRegistrator

    class A(metaclass=CommandRegistrator): pass
    class B(metaclass=CommandRegistrator): pass
    class C(B): pass
    class D(B): pass
    classes = type('Classes', (object,), {'A': A, 'B': B, 'C': C, 'D': D,
                                          '__iter__': lambda self: iter([getattr(self, x) for x in 'ABCD'])})()
    assert all([type(x) == CommandRegistrator for x in classes])  # sanity check
    assert all([isinstance(x, CommandRegistrator) for x in classes])  # sanity check

    class P1(CommandRegistrator): pass
    return {'correct': classes, 'wrong': P1}


def test_command_registrator(assert_different_objects, classes, modify_registry):
    classes = classes['correct']
    assert all([hasattr(x, 'registry') for x in classes])
    assert all([hasattr(x, 'state') for x in classes])
    assert_different_objects([c.registry for c in classes])

    values = [1, 2, 3, 4]
    [setattr(getattr(classes, c), 'state', v) for v, c in zip(values, 'ABCD')]
    assert_different_objects([c.state for c in classes])

    [modify_registry(getattr(classes, c).registry, c.lower(), v) for v, c in zip(values, 'ABCD')]
    assert classes.B.registry != classes.A.registry != classes.C.registry != classes.D.registry

    assert classes.A.__getitem__('a') == 1
    assert classes.B.__getitem__('b') == 2
    assert classes.C.__getitem__('c') == 3
    assert classes.D.__getitem__('d') == 4
    assert 'b' not in classes.C.registry
    assert 'c' not in classes.B.registry
    assert 'c' not in classes.D.registry
    assert 'd' not in classes.C.registry
    assert classes.A['a'] == 1
    assert classes.B['b'] == 2
    assert classes.C['c'] == 3
    assert classes.D['d'] == 4


def test_wrong_command_registrator_usage(classes):
    assert type(classes['wrong']) == type
    assert not hasattr(classes['wrong'], 'state')
    assert not hasattr(classes['wrong'], 'state')
