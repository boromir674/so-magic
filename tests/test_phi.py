import pytest

@pytest.fixture
def registering_phi_at_the_same_key_error():
    from green_magic.utils.registry import ObjectRegistryError
    return ObjectRegistryError


def test_phi_creation(registering_phi_at_the_same_key_error):
    from green_magic.data.features.phi import PhiFunction, phi_registry

    assert phi_registry.objects == {}
    assert 'pame' not in phi_registry

    @PhiFunction.register('pame')
    def ela(x):
        """ela Docstring"""
        return x + 1

    assert 'pame' in phi_registry
    assert ela.__name__ == 'ela'
    assert ela.__doc__ == 'ela Docstring'

    @PhiFunction.register('')
    def gg(x):
        return x * 2
    assert 'gg' in phi_registry

    @PhiFunction.register()
    def dd(x):
        return x * 2
    assert 'dd' in phi_registry

    @PhiFunction.register('edw')
    class Edw:
        def __call__(self, data, **kwargs):
            return data + 5
    assert 'edw' in phi_registry
    assert phi_registry.get('edw')(3) == 8

    @PhiFunction.register('')
    class qw:
        def __call__(self, data, **kwargs):
            return data - 5
    assert phi_registry.get('qw')(3) == -2
    assert 'qw' in phi_registry

    @PhiFunction.register()
    class Nai:
        def __call__(self, data, **kwargs):
            return data - 5
    assert 'Nai' in phi_registry

    with pytest.raises(registering_phi_at_the_same_key_error):
        @PhiFunction.register()
        def gg(x):
            return x

    assert phi_registry.get('gg')(1) == 2
