import pytest
from green_magic.data.features.phi import PhiFunction


def test_phi_creation():
    from green_magic.data.features.phi import phi_registry
    assert phi_registry.objects == {}
    @PhiFunction.register('aa')
    def ela(x):
        """ela Docstring"""
        return x + 1

    assert 'aa' in phi_registry
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
    from green_magic.utils import ObjectRegistryError
    with pytest.raises(ObjectRegistryError):
        @PhiFunction.register()
        def gg(x):
            return x

    assert phi_registry.get('gg')(1) == 2
