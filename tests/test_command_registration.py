import pytest


@pytest.fixture
def command_registrator():
    from so_magic.data.backend.backend import CommandRegistrator
    return CommandRegistrator


def test_command_registrator(assert_different_objects, command_registrator):
    class A(metaclass=command_registrator): pass
    class B(metaclass=command_registrator): pass
    class C(B): pass
    class D(B): pass
    classes = (A, B, C, D)

    assert all([hasattr(x, 'registry') for x in classes])
    assert all([type(x) == command_registrator for x in classes])
    assert all([hasattr(x, 'state') for x in classes])
    assert_different_objects([A.registry, B.registry, C.registry, D.registry])

    A.state = 1
    B.state = 2
    C.state = 3
    D.state = 4
    assert_different_objects([A.state, B.state, C.state, D.state])

    A.registry['a'] = 1
    B.registry['b'] = 2
    C.registry['c'] = 3
    D.registry['d'] = 4
    assert B.registry != A.registry != C.registry != D.registry

    assert A.__getitem__('a') == 1
    assert B.__getitem__('b') == 2
    assert C.__getitem__('c') == 3
    assert D.__getitem__('d') == 4
    assert 'b' not in C.registry
    assert 'c' not in B.registry
    assert 'c' not in D.registry
    assert 'd' not in C.registry
    assert A['a'] == 1
    assert B['b'] == 2
    assert C['c'] == 3
    assert D['d'] == 4

    class P1(command_registrator): pass
    assert type(P1) == type
    assert not hasattr(P1, 'state')
    assert not hasattr(P1, 'state')


def test_wrong_command_registrator_usage(command_registrator):
    class P1(command_registrator): pass
    assert type(P1) == type
    assert not hasattr(P1, 'state')
    assert not hasattr(P1, 'state')
