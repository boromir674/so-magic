import os
import pytest


my_dir = os.path.dirname(os.path.realpath(__file__))

####### Files and folders
@pytest.fixture
def tests_root_dir():
    return my_dir

@pytest.fixture
def tests_data_root(tests_root_dir):
    return os.path.join(tests_root_dir, 'dts')


@pytest.fixture
def sample_json(tests_data_root):
    return os.path.join(tests_data_root, 'sample-strains.jl')

@pytest.fixture
def sample_collaped_json(tests_data_root):
    return os.path.join(tests_data_root, 'sample-strains-colapsed.jl')


@pytest.fixture()
def test_json_data(sample_json):
    return {
        'file_path': sample_json,
        'nb_lines': 100,
        'attributes': {'flavors', 'name', 'medical', 'description', 'image_urls', 'parents', 'negatives', 'grow_info', '_id', 'type', 'image_paths', 'effects'},
    }


@pytest.fixture
def r_data_manager():
    from green_magic.data.data_manager import DataManager



@pytest.fixture
def data_manager():
    from green_magic.data.backend import Backend, DataEngine, pd_engine
    from green_magic.data.data_manager import DataManager
    from green_magic.data.commands_manager import CommandsManager
    from green_magic.data.dataset import DatapointsFactory
    from green_magic.data.command_factories import MagicCommandFactory
    from green_magic.data.features.phi import PhiFunction

    data_api = DataManager(Backend(DataEngine.create('test_pd')))

    datapoints_fact = data_api.backend.engine.__class__.datapoints_factory
    cmd_fact = DataEngine.test_pd.command_factory
    assert isinstance(datapoints_fact, DatapointsFactory)
    assert isinstance(cmd_fact, MagicCommandFactory)

    subjects = [datapoints_fact.subject, cmd_fact, PhiFunction.subject]
    assert len(set([id(x._observers) for x in subjects])) == len(subjects)

    for s in subjects:
        s._observers = []
        # print('FFFF', type(s), id(s), id(s._observers), len(s._observers))
    assert all(len(x._observers) == 0 for x in subjects)

    data_api.backend.engine.__class__.datapoints_factory.subject.attach(data_api.backend.datapoints_manager)
    DataEngine.test_pd.command_factory.attach(data_api.commands_manager.command.accumulator)
    PhiFunction.subject.attach(data_api.phis)

    print(f"dtp-fact: {type(datapoints_fact)} -> observers: [{', '.join(str(_) for _ in datapoints_fact.subject._observers)}]")
    print(
        f"cmd-fact: {type(cmd_fact)} -> observers: [{', '.join(str(_) for _ in cmd_fact._observers)}]")
    print('----------------------')
    print(
        f"dtp-fact: {type(datapoints_fact)} -> observers: [{', '.join(str(_) for _ in datapoints_fact.subject._observers)}]")
    print(
        f"cmd-fact: {type(cmd_fact)} -> observers: [{', '.join(str(_) for _ in cmd_fact._observers)}]")


    assert datapoints_fact.subject._observers[0] == data_api.backend.datapoints_manager
    assert cmd_fact._observers[0] == data_api.commands_manager.command.accumulator

    assert all(len(x._observers) == 1 for x in subjects)

    return data_api


@pytest.fixture
def test_engine(data_manager):
    from green_magic.data.backend import DataEngine
    from green_magic.data.backend.panda_handling.df_backend import PDTabularIterator, PDTabularRetriever, PDTabularMutator
    DataEngine.new('test_pd')
    DataEngine.test_pd.retriever = PDTabularRetriever
    DataEngine.test_pd.iterator = PDTabularIterator
    DataEngine.test_pd.mutator = PDTabularMutator
    subjects = [
        data_manager.backend.engine.__class__.datapoints_factory.subject,
        DataEngine.test_pd.command_factory,
    ]
    for s in subjects:
        for o in s._observers:
            s.detach(o)

    subjects[0].attach(data_manager.backend.datapoints_manager)
    subjects[1].attach(data_manager.commands_manager.command.accumulator)

    assert all([len(x) == 1 for x in (
        data_manager.backend.engine.__class__.datapoints_factory.subject._observers,
        DataEngine.test_pd.command_factory._observers,
    )])
    # DataEngine.test_pd.command_factory(data_structure, res, [_ for _ in []],
    #                                                                cls.retriever(),
    #                                                                cls.iterator(),
    #                                                                cls.mutator())
    return DataEngine.test_pd


@pytest.fixture
def define_observations_command(test_engine):
    import pandas as pd
    @test_engine.dec()
    def observations(file_path):
        return pd.read_json(file_path, lines=True)
    assert 'observations' in test_engine.registry
    assert len(test_engine.registry) == 1


@pytest.fixture
def datapoints(data_manager, define_observations_command, test_json_data):
    cmd = data_manager.command.observations
    cmd.args = [test_json_data['file_path']]

    from green_magic.utils.commands import Invoker, CommandHistory

    inv = Invoker(CommandHistory())
    inv.execute_command(cmd)
    return data_manager.backend.datapoints_manager.datapoints

# Helpers
@pytest.fixture
def factories():
    def factories_dict(data_manager_instance):
        return {'cmd': DataEngine.test_pd.command_factory}