import pytest
from green_magic.data.commands_manager import CommandsManager
from green_magic.data.backend import Backend, DataEngine
from green_magic.data.data_manager import DataManager
from green_magic.data.backend import panda_handling


@pytest.fixture()
def test_json_data(sample_json):
    return {
        'file_path': sample_json,
        'nb_lines': 100,
        'attributes': {'flavors', 'name', 'medical', 'description', 'image_urls', 'parents', 'negatives', 'grow_info', '_id', 'type', 'image_paths', 'effects'},
    }

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
        assert id(getattr(DataEngine.test_pd, x)) != id(getattr(DataEngine.data_lib, x)) != id(DataEngine.registry)

    assert id(DataEngine.test_pd.datapoints_factory) == id(DataEngine.data_lib.datapoints_factory)

    import pandas as pd
    @DataEngine.test_pd.command
    def observations(file_path):
        return pd.read_json(file_path, lines=True)

    # TODO uncomment below
    # assert len(DataEngine.test_pd.registry) == 1
    # assert len(DataEngine.data_lib.registry) == 0

    # assert all(id(getattr(DataEngine.test_pd, x) != id(getattr(DataEngine.data_lib, x)) for x in ATTRS))


def test_data_manager(test_json_data):
    import types
    from green_magic.utils.commands import Command
    from green_magic.data.backend.panda_handling.df_backend import PDTabularIterator, PDTabularRetriever, PDTabularReporter
    from green_magic.data.features.phi import PhiFunction

    DataEngine.new('test_pd')
    assert 'test_pd' in DataEngine.subclasses
    assert hasattr(DataEngine, 'state')
    assert hasattr(DataEngine, 'registry')

    data_api = DataManager(CommandsManager(), Backend(DataEngine.create('test_pd')))
    # make the datapoint_manager listen to newly created Datapoints objects events
    assert hasattr(data_api, 'commands_manager')
    assert hasattr(data_api.commands_manager, 'command')
    assert hasattr(data_api.backend, 'datapoints_manager')

    data_api.backend.engine.__class__.datapoints_factory.subject.attach(data_api.backend.datapoints_manager)
    DataEngine.test_pd.command_factory.attach(data_api.commands_manager.command.accumulator)
    PhiFunction.subject.attach(data_api.phis)

    assert data_api.backend.engine.__class__.datapoints_factory not in PhiFunction.subject._observers

    # test runtime command registration
    import pandas as pd
    @DataEngine.test_pd.dec()
    def observations(file_path):
        return pd.read_json(file_path, lines=True)

    @DataEngine.test_pd.dec()
    def add_attribute(_datapoints, values, new_attribute):
        print("CORRECT")
        _datapoints.observations[new_attribute] = values

    assert type(DataEngine.test_pd) == type(DataEngine)
    assert type(DataEngine.test_pd.registry) == dict
    assert type(DataEngine.test_pd._commands) == dict
    assert 'observations' in DataEngine.test_pd.registry
    assert 'observations' in DataEngine.test_pd._commands
    assert 'observations' not in DataEngine.registry

    assert type(DataEngine.test_pd._commands['observations']) == Command

    cmd = DataEngine.test_pd._commands['observations']
    # cmd = data_api.command.observations
    cmd.args = [test_json_data['file_path']]

    assert type(cmd._receiver) == types.FunctionType
    assert cmd._method == '__call__'
    assert cmd.args == [test_json_data['file_path']]

    from green_magic.utils.commands import Invoker, CommandHistory

    DataEngine.test_pd.retriever = PDTabularRetriever
    DataEngine.test_pd.iterator = PDTabularIterator
    DataEngine.test_pd.reporter = PDTabularReporter

    inv = Invoker(CommandHistory())
    inv.execute_command(cmd)

    datapoints = data_api.backend.datapoints_manager.datapoints
    assert len(datapoints) == test_json_data['nb_lines']
    print(datapoints.attributes)

    assert set(datapoints.attributes) == test_json_data['attributes']

    assert 'add_attribute' in DataEngine.test_pd.registry

    cmd1 = DataEngine.test_pd._commands['add_attribute']
    # cmd1 = data_api.command.observations
    cmd1.args = [datapoints, [_ for _ in range(1, len(datapoints) + 1)], 'test_attr']

    cmd1.execute()

    assert set(datapoints.attributes) == set(_ for _ in list(test_json_data['attributes']) + ['test_attr'])
