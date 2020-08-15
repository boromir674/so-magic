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


def test_data_manager(sample_json):
    import types
    from green_magic.utils.commands import Command
    from green_magic.data.backend.panda_handling.df_backend import PDTabularIterator, PDTabularRetriever
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
    # PhiFunction.subject.attach(data_api.phis)
    
    # test runtime command registration
    import pandas as pd
    @DataEngine.test_pd.dec()
    def observations(file_path):
        return pd.read_json(file_path, lines=True)

    assert type(DataEngine.test_pd) == type(DataEngine)
    assert type(DataEngine.test_pd.registry) == dict
    assert type(DataEngine.test_pd._commands) == dict
    assert 'observations' in DataEngine.test_pd.registry
    assert 'observations' in DataEngine.test_pd._commands
    assert 'observations' not in DataEngine.registry

    assert type(DataEngine.test_pd._commands['observations']) == Command

    cmd = DataEngine.test_pd._commands['observations']
    # cmd = data_api.command.observations
    cmd.args = [sample_json]

    assert type(cmd._receiver) == types.FunctionType
    assert cmd._method == '__call__'
    assert cmd.args == [sample_json]

    from green_magic.utils.commands import Invoker, CommandHistory

    DataEngine.test_pd.retriever = PDTabularRetriever()
    DataEngine.test_pd.iterator = PDTabularIterator()

    inv = Invoker(CommandHistory())
    inv.execute_command(cmd)

    assert len(data_api.backend.datapoints_manager.datapoints) == 100

    # from green_magic.data.features.phi import PhiFunction

