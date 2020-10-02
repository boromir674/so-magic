import pytest


def test_engine_registration():
    from so_magic.data.backend import DataEngine
    from so_magic.data.backend.engine import EngineType
    assert type(EngineType) == type
    assert type(DataEngine) == EngineType
    from so_magic.data.command_factories import CommandRegistrator

    ATTRS = ('registry', '_commands', 'command')
    DataEngine.new('test_pd')
    assert 'test_pd' in DataEngine.subclasses
    assert type(DataEngine.test_pd) == type(DataEngine)
    assert all(hasattr(DataEngine.test_pd, x) for x in ATTRS)

    DataEngine.new('data_lib')
    assert 'data_lib' in DataEngine.subclasses
    assert type(DataEngine.data_lib) == type(DataEngine)
    assert all(hasattr(DataEngine.data_lib, x) for x in ATTRS)

    for x in ATTRS:
        print(getattr(DataEngine.test_pd, x), getattr(DataEngine.data_lib, x))
        assert id(getattr(DataEngine.test_pd, x)) != id(getattr(DataEngine.data_lib, x)) != id(DataEngine.registry)

    assert len(DataEngine.test_pd.registry) == 0
    assert len(DataEngine.data_lib.registry) == 0
