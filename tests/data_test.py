import pytest

@pytest.fixture
def datapoint():
    from green_magic.strain.strain_class import Strain
    _ = Strain('og-kush', 'Og Kush', 'hybrid', ['flavor1', 'flavor2'], ['ef1', 'ef2'], ['n1'], ['m1', 'm2', 'm3'], ['p1', 'p2'], '100-200', '7-9', '251-500', '>2', 'Moderate', [], '')
    print(_)
    return _


def test_datapoint(datapoint):
    print("DASDASD")
    assert datapoint.name == 'Og Kush'
    # assert datapoint.stretch[0] == 100
    # assert datapoint.stretch.lower == 100
    assert hasattr(datapoint, 'images')
    print('\n'.join([_ for _ in dir(datapoint)]))
