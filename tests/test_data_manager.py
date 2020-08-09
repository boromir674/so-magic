from green_magic.data.commands_manager import CommandsManager
from green_magic.data.backend import Backend, DataEngine
from green_magic.data.data_manager import DataManager
from green_magic.data.backend import panda_handling

print("!1111111", DataEngine.subclasses)


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
    assert type(DataEngine.test_pd.registry) == dict
    assert type(DataEngine.test_pd._commands) == dict
    assert 'observations' in DataEngine.test_pd._commands
    # assert 'observations' in DataEngine.test_pd.registry

    data_api = DataManager(CommandsManager(), Backend(DataEngine.create('pd')))
    # make the datapoint_manager listen to newly created Datapoints objects events
    data_api.backend.engine.datapoints_factory.subject.attach(data_api.backend.datapoints_manager)