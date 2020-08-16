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
