import pytest


@pytest.fixture
def command_registrator():
    from so_magic.data.backend.backend import CommandRegistrator
    return CommandRegistrator


@pytest.fixture
def modify_registry():
    def _modify_registry(registry, key, value):
        registry[key] = value
    return _modify_registry


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


@pytest.fixture
def assert_retrieved():
    def _assert_retrieved(getter, classes, keys, expected_values):
        assert all(getter(c, l) == v for c, l, v in zip(classes, keys, expected_values))
    return _assert_retrieved


def test_command_registrator(assert_different_objects, classes, modify_registry, assert_retrieved):
    assert all([hasattr(x, 'registry') for x in classes])
    assert all([hasattr(x, 'state') for x in classes])
    assert_different_objects([c.registry for c in classes])

    values = [1, 2, 3, 4]
    [setattr(getattr(classes, c), 'state', v) for v, c in zip(values, 'ABCD')]
    assert_different_objects([c.state for c in classes])

    [modify_registry(getattr(classes, c).registry, c.lower(), v) for v, c in zip(values, 'ABCD')]
    assert classes.B.registry != classes.A.registry != classes.C.registry != classes.D.registry

    assert_retrieved(lambda c, l: c.__getitem__(l), classes, keys='abcd', expected_values=values)
    assert_retrieved(lambda c, l: c[l], classes, keys='abcd', expected_values=values)

    # assert_not_in_registry()

    assert 'b' not in classes.C.registry
    assert 'c' not in classes.B.registry
    assert 'c' not in classes.D.registry
    assert 'd' not in classes.C.registry


def test_wrong_command_registrator_usage(command_registrator):
    class P1(command_registrator): pass
    assert type(P1) == type
    assert not hasattr(P1, 'state')
    assert not hasattr(P1, 'state')
