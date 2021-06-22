import pytest


@pytest.fixture
def command_registrator():
    from so_magic.data.backend.backend import CommandRegistrator
    return CommandRegistrator


@pytest.fixture
def classes(command_registrator):
    class A(metaclass=command_registrator): pass
    class B(metaclass=command_registrator): pass
    class C(B): pass
    class D(B): pass
    classes = type('Classes', (object,), {'A': A, 'B': B, 'C': C, 'D': D,
                                          '__iter__': lambda self: iter([getattr(self, x) for x in 'ABCD'])})()
    assert all([type(x) == command_registrator for x in classes])  # sanity check
    assert all([isinstance(x, command_registrator) for x in classes])  # sanity check
    return classes


def test_command_registrator(assert_different_objects, classes):
    assert all([hasattr(x, 'registry') for x in classes])
    assert all([hasattr(x, 'state') for x in classes])
    assert_different_objects([c.registry for c in classes])

    classes.A.state = 1
    classes.B.state = 2
    classes.C.state = 3
    classes.D.state = 4
    assert_different_objects([c.state for c in classes])

    classes.A.registry['a'] = 1
    classes.B.registry['b'] = 2
    classes.C.registry['c'] = 3
    classes.D.registry['d'] = 4
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


def test_wrong_command_registrator_usage(command_registrator):
    class P1(command_registrator): pass
    assert type(P1) == type
    assert not hasattr(P1, 'state')
    assert not hasattr(P1, 'state')
