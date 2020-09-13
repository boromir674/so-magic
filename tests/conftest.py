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
def somagic():
    from so_magic import init_so_magic
    _ = init_so_magic()
    return _


@pytest.fixture
def data_manager():
    def getter():
        from so_magic.data import init_data_manager
        from so_magic.data.backend import init_backend

        data_manager = init_data_manager(init_backend(engine_type='pd'))

        datapoints_fact = data_manager.backend.datapoints_factory
        cmd_fact = data_manager.backend.engine.command_factory

        # test 1
        from so_magic.data.dataset import DatapointsFactory
        from so_magic.data.command_factories import MagicCommandFactory

        assert isinstance(datapoints_fact, DatapointsFactory)
        assert isinstance(cmd_fact, MagicCommandFactory)

        subjects = [datapoints_fact.subject, cmd_fact, data_manager.phi_class.subject]
        assert len(set([id(x._observers) for x in subjects])) == len(subjects)

        assert datapoints_fact.subject._observers[0] == data_manager.backend.datapoints_manager
        assert cmd_fact._observers[0] == data_manager.commands_manager.command.accumulator
        assert data_manager.phi_class.subject._observers[0] == data_manager.built_phis

        print(f"DTP FCT OBS: [{', '.join(str(_) for _ in datapoints_fact.subject._observers)}]")
        print(f"CMD FCT OBS: [{', '.join(str(_) for _ in cmd_fact._observers)}]")
        print(f"PHIFUNC class OBS: [{', '.join(str(_) for _ in data_manager.phi_class.subject._observers)}]")
        assert all([len(x._observers) == 1 for x in subjects])
        return data_manager

    return getter


# Helpers
@pytest.fixture
def factories():
    def factories_dict(data_manager_instance):
        return {'cmd': DataEngine.test_pd.command_factory}