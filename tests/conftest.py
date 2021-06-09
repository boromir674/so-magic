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

# Test data
@pytest.fixture
def sample_json(tests_data_root):
    return os.path.join(tests_data_root, 'sample-data.jsonlines')

@pytest.fixture
def sample_collaped_json(tests_data_root):
    return os.path.join(tests_data_root, 'sample-data-collapsed.jsonlines')


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
        from so_magic.data.backend import init_engine

        data_manager = init_data_manager(init_engine(engine_type='pd'))

        datapoints_fact = data_manager.engine.backend.datapoints_factory
        cmd_fact = data_manager.engine.backend.command_factory

        # test 1
        from so_magic.data.datapoints.datapoints import DatapointsFactory
        from so_magic.data.backend.engine_command_factory import MagicCommandFactory

        assert isinstance(datapoints_fact, DatapointsFactory)
        assert isinstance(cmd_fact, MagicCommandFactory)

        subjects = [datapoints_fact.subject, cmd_fact, data_manager.phi_class.subject]
        assert len(set([id(x._observers) for x in subjects])) == len(subjects)

        assert datapoints_fact.subject._observers[0] == data_manager.engine.datapoints_manager
        assert cmd_fact._observers[0] == data_manager.commands_manager.command.accumulator
        assert data_manager.phi_class.subject._observers[0] == data_manager.built_phis

        print(f"DTP FCT OBS: [{', '.join(str(_) for _ in datapoints_fact.subject._observers)}]")
        print(f"CMD FCT OBS: [{', '.join(str(_) for _ in cmd_fact._observers)}]")
        print(f"PHIFUNC class OBS: [{', '.join(str(_) for _ in data_manager.phi_class.subject._observers)}]")
        assert all([len(x._observers) == 1 for x in subjects])
        return data_manager

    return getter


@pytest.fixture
def test_data_manager(data_manager):
    return data_manager()


@pytest.fixture
def load_test_data(test_data_manager, sample_json):
    def load_data(json_lines_formatted_file_path):
        cmd = test_data_manager.command.observations_command
        cmd.args = [json_lines_formatted_file_path]
        cmd.execute()
    return lambda: load_data(sample_json)


@pytest.fixture
def read_observations():
    """Read a json lines formatted file and create the observations object (see Datapoints class)."""
    def load_data(so_master, json_lines_formatted_file_path):
        """Create the observations object for a Datapoints instance, given a data file.

        Args:
            so_master (so_magic.so_master.SoMaster): an instance of SoMaster
            json_lines_formatted_file_path (str): path to a json lines formatted file with the observations data
        """
        cmd = so_master.command.observations_command
        cmd.args = [json_lines_formatted_file_path]
        cmd.execute()
    return load_data


@pytest.fixture
def test_datapoints(read_observations, sample_collaped_json, somagic):
    """Read the designated json lines 'test file' (which contains the 'test observations') as a Datapoints instance."""
    read_observations(somagic, sample_collaped_json)
    return somagic.datapoints


@pytest.fixture
def built_in_backends():
    from so_magic.data.backend.panda_handling.df_backend import magic_backends
    engine_backends = magic_backends()
    return engine_backends
