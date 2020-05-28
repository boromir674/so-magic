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
def sample_json():
    return os.path.join(tests_data_root, 'sample-strains.jl')


#### Objects to use for test scenarios

@pytest.fixture
def green_master():
    from green_magic import GreenMaster
    return GreenMaster()

@pytest.fixture
def command_invoker(green_master):
    return green_master.invoker


###### Built data to test

@pytest.fixture
def og_kush():
    from green_magic.strain.strain_class import Strain
    return Strain('og-kush', 'Og Kush', 'hybrid', ['flavor1', 'flavor2'], ['ef1', 'ef2'], ['n1'], ['m1', 'm2', 'm3'], ['p1', 'p2'], '100-200', '7-9', '251-500', '>2', 'Moderate', [], '')
