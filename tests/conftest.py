from glob import glob
import pytest


def file_path_to_module_path(string: str) -> str:
    return string.replace("/", ".").replace("\\", ".").replace(".py", "")


pytest_plugins = [
    file_path_to_module_path(fixture) for fixture in glob("tests/fixtures/*.py") if "__" not in fixture
]


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
        return data_manager
    return getter


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
def test_dataset(somagic, read_observations, sample_collaped_json):
    """Dataset ready to be fed into a training/inference algorithm; feature vectors have been computed."""
    read_observations(somagic, sample_collaped_json)

    type_values = ['hybrid', 'indica', 'sativa']
    ATTRS2 = [f'type_{x}' for x in type_values]
    from functools import reduce
    UNIQUE_FLAVORS = reduce(lambda i, j: set(i).union(set(j)),
                            [_ for _ in somagic._data_manager.datapoints.observations['flavors'] if _ is not None])

    # cmd = somagic._data_manager.command.encode_command
    # cmd.args = [somagic._data_manager.datapoints, 'type']
    # cmd.execute()
    #
    # cmd = somagic._data_manager.command.replace_empty_command
    # cmd.args = [somagic._data_manager.datapoints, 'flavors', []]
    # cmd.execute()
    #
    # cmd = somagic._data_manager.command.encode_command
    # cmd.args = [somagic._data_manager.datapoints, 'flavors']
    # cmd.execute()


    cmd = somagic._data_manager.command.select_variables_command
    # current limitations:
    # 1. client code has to know the number of distict values for the nominal variable 'type'
    # 2. client code has to provide the column names that will result after encoding the 'type' variable
    cmd.args = [[
        # current limitations:
        # 1. client code has to know the number of distict values for the nominal variable 'type'
        # 2. client code has to provide the column names that will result after encoding the 'type' variable
        {'variable': 'type', 'columns': ATTRS2},
        # current limitations:
        # 1. client code has to know the number of distict values for the nominal variable 'flavors'
        # 2. client code has to provide the column names that will result after encoding the 'flavors' variable
        {'variable': 'flavors', 'columns': list(UNIQUE_FLAVORS)}]]
    cmd.execute()

    cmd = somagic._data_manager.command.one_hot_encoding_command
    cmd.args = [somagic._data_manager.datapoints, 'type']
    cmd.execute()

    assert set([type(x) for x in somagic._data_manager.datapoints.observations['flavors']]) == {list, type(None)}

    nb_columns_before = len(somagic._data_manager.datapoints.observations.columns)

    cmd = somagic._data_manager.command.one_hot_encoding_list_command
    cmd.args = [somagic._data_manager.datapoints, 'flavors']
    cmd.execute()

    assert nb_columns_before + len(UNIQUE_FLAVORS) == len(somagic._data_manager.datapoints.observations.columns)

    import numpy as np
    setattr(somagic.dataset, 'feature_vectors',
            np.array(somagic._data_manager.datapoints.observations[ATTRS2 + list(UNIQUE_FLAVORS)]))

    MAX_FLAVORS_PER_DAATPOINT = max(
        [len(x) for x in [_ for _ in somagic._data_manager.datapoints.observations['flavors'] if type(_) is list]])
    return somagic.dataset, type_values, UNIQUE_FLAVORS, MAX_FLAVORS_PER_DAATPOINT, nb_columns_before


@pytest.fixture
def built_in_backends():
    from so_magic.data.backend.panda_handling.df_backend import magic_backends
    engine_backends = magic_backends()
    return engine_backends


@pytest.fixture
def tabular_operators(built_in_backends):
    operators = {
        'retriever': {
            'class': built_in_backends.backend_interfaces['retriever']['class_registry'].subclasses['pd'],
            'interface': {
                'column': '(identifier, data)',
                'row': '(identifier, data)',
                'nb_columns': '(data)',
                'nb_rows': '(data)',
                'get_numerical_attributes': '(data)',
            }
        },
        'iterator': {
            'class': built_in_backends.backend_interfaces['iterator']['class_registry'].subclasses['pd'],
            'interface': {
                'columnnames': '(data)',
                'itercolumns': '(data)',
                'iterrows': '(data)',
            },
        },
        'mutator': {
            'class': built_in_backends.backend_interfaces['mutator']['class_registry'].subclasses['pd'],
            'interface': {
                'add_column': '(datapoints, values, new_attribute, **kwargs)',
            },
        },
    }
    return {
        'operators': operators,
        'reverse_dict': {operator_dict['class']: key for key, operator_dict in operators.items()},
        'get_nb_args': lambda operator_interface_name, method_name: len(operators[operator_interface_name]['interface'][method_name].replace(', **kwargs', '').split(',')),
        # operator_name_2_required_methods
        'required_methods': iter(((operator_interface_name, v['interface'].keys())
                                  for operator_interface_name, v in operators.items()))
    }


@pytest.fixture
def assert_different_objects():
    def _assert_different_objects(objects):
        assert len(set([id(x) for x in objects])) == len(objects)
    return _assert_different_objects
