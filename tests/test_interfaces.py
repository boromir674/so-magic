import pytest
from green_magic.interfaces import *

@pytest.fixture
def defined_interfaces():
    return {
        'norm': Normalization,
        'disc': Discretization,
        'enc': Encoding
    }

@pytest.fixture
def correct_interface_implementations(defined_interfaces):
    class AbstractNormalizer(defined_interfaces['norm']): pass
    class AbstractDiscretizer(defined_interfaces['disc']): pass
    class AbstractEncoder(defined_interfaces['enc']): pass
    class ConcreteNormalizer:
        def normalize(self, *args, **kwargs): pass
    return {'norm': (AbstractNormalizer, ConcreteNormalizer), 'disc': (AbstractDiscretizer,), 'enc': (AbstractEncoder,)}


def test_subclasses(defined_interfaces, correct_interface_implementations):
    for k, interface in defined_interfaces.items():
        assert all(issubclass(x, interface) for x in correct_interface_implementations[k])
