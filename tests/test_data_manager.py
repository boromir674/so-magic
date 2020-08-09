from green_magic.data.commands_manager import CommandsManager
from green_magic.data.backend import Backend, DataEngine
from green_magic.data.data_manager import DataManager
from green_magic.data.backend import panda_handling


def test_engine_registration():
    from green_magic.data.backend import DataEngine
    from green_magic.data.backend.engine import EngineType
    assert type(DataEngine) == EngineType
    from green_magic.data.commands_manager import CommandRegistrator

    # type(type(DataEngine))
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
        assert id(getattr(DataEngine.test_pd, x)) != id(getattr(DataEngine.data_lib, x))

    assert id(DataEngine.test_pd.datapoints_factory) == id(DataEngine.data_lib.datapoints_factory)

    import pandas as pd
    @DataEngine.test_pd.command
    def observations(file_path):
        return pd.read_json(file_path, lines=True)

    # TODO uncomment below
    # assert len(DataEngine.test_pd.registry) == 1
    # assert len(DataEngine.data_lib.registry) == 0

    # assert all(id(getattr(DataEngine.test_pd, x) != id(getattr(DataEngine.data_lib, x)) for x in ATTRS))


def test_data_manager():

    DataEngine.new('test_pd')
    assert 'test_pd' in DataEngine.subclasses
    assert hasattr(DataEngine, 'state')
    assert hasattr(DataEngine, 'registry')
    import pandas as pd
    @DataEngine.test_pd.command
    def observations(file_path):
        return pd.read_json(file_path, lines=True)

    assert type(DataEngine.test_pd) == type(DataEngine)
    # assert type(DataEngine.test_pd.registry) == dict
    assert type(DataEngine.test_pd._commands) == dict
    # assert 'observations' in DataEngine.test_pd._commands
    # assert 'observations' in DataEngine.test_pd.registry

    data_api = DataManager(CommandsManager(), Backend(DataEngine.create('test_pd')))
    # make the datapoint_manager listen to newly created Datapoints objects events
    data_api.backend.engine.datapoints_factory.subject.attach(data_api.backend.datapoints_manager)