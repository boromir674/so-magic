import os
import pytest


my_dir = os.path.dirname(os.path.realpath(__file__))

####### FIles and folders
@pytest.fixture
def tests_root():
    return my_dir

@pytest.fixture
def tests_data_root(tests_root):
    return os.path.join(tests_root, 'dts')


@pytest.fixture
def sample_json(tests_data_root):
    return os.path.join(tests_data_root, 'sample-strains.jl')


#### Objects to use for test scenarios

@pytest.fixture
def som_master():
    from green_magic.data.backend import DataEngine
    DataEngine.new('pd')
    from green_magic.strainmaster import StrainMaster
    return StrainMaster()


@pytest.fixture
def load_sample_datapoints_cmd(som_master, sample_json):
    from green_magic.data.backend import DataEngine
    DataEngine.new('pd')
    import pandas
    @DataEngine.pd.command
    def observations(file_path):
        return pandas.read_json(file_path, lines=True)
    command = som_master.commands.observations
    command.append_arg(sample_json)
    return command


@pytest.fixture
def compute_feature_vectors_cmd(som_master):
    command = som_master.commands.feature_vectors
    return command


@pytest.fixture
def sample_datapoints(som_master, load_sample_datapoints_cmd):
    """Use this fixture to get a Datapoints object costructed from the 'samples-strains.jl' test file in 'dts' folder."""
    som_master.engine.invoker.execute_command(load_sample_datapoints_cmd)

@pytest.fixture
def sample_feature_vectors(som_master, compute_feature_vectors_cmd):
    """Use this fixture to compute the feature vectors of the sample-straions.jl."""
    som_master.engine.invoker.execute_command(compute_feature_vectors_cmd)


@pytest.fixture
def command_invoker(green_master):
    return green_master.invoker


###### Built data to test

@pytest.fixture
def og_kush():
    from green_magic.strain.strain_class import Strain
    return Strain('og-kush', 'Og Kush', 'hybrid', ['flavor1', 'flavor2'], ['ef1', 'ef2'], ['n1'], ['m1', 'm2', 'm3'], ['p1', 'p2'], '100-200', '7-9', '251-500', '>2', 'Moderate', [], '')
