import pytest


@pytest.fixture
def registering_phi_at_the_same_key_error():
    from so_magic.utils.registry import ObjectRegistryError
    return ObjectRegistryError


@pytest.fixture
def app_phi_function(somagic):
    return somagic._data_manager.phi_class


def test_phi_creation(app_phi_function, registering_phi_at_the_same_key_error):
    from so_magic.data.features.phi import phi_registry

    assert phi_registry.objects == {}
    assert 'pame' not in phi_registry

    PhiFunction = app_phi_function

    @PhiFunction.register('pame')
    def ela(x):
        """ela Docstring"""
        return x + 1

    assert 'pame' in phi_registry
    assert ela.__name__ == 'ela'
    assert ela.__doc__ == 'ela Docstring'

    assert phi_registry.get('pame').__name__ == 'ela'
    assert phi_registry.get('pame').__doc__ == 'ela Docstring'
    test_value = 5
    assert phi_registry.get('pame')(test_value) == test_value + 1

    @PhiFunction.register('')
    def gg(x):
        return x * 2
    assert 'gg' in phi_registry

    @PhiFunction.register()
    def dd(x):
        return x * 2
    assert 'dd' in phi_registry
    assert phi_registry.get('dd')(4) == 8

    @PhiFunction.register('edw')
    class Edw:
        def __call__(self, data, **kwargs):
            return data + 5
    assert 'edw' in phi_registry
    assert phi_registry.get('edw')(3) == 8

    @PhiFunction.register('')
    class qw:
        def __call__(self, data, **kwargs):
            """Subtract 5 from the input number.

            Args:
                data ([type]): numerical value

            Returns:
                [type]: the result of the subtraction
            """
            return data - 5
    
    assert 'qw' in phi_registry
    assert phi_registry.get('qw')(3) == -2

    assert phi_registry.get('qw').__name__ == 'qw'
    assert phi_registry.get('qw').__doc__ == qw.__call__.__doc__

    @PhiFunction.register()
    class Nai:
        def __call__(self, data, **kwargs):
            """Subtract 1 to the input number."""            
            return data - 1

    assert 'Nai' in phi_registry
    assert phi_registry.get('Nai').__name__ == 'Nai'
    assert phi_registry.get('Nai').__doc__ == 'Subtract 1 to the input number.'
    
    assert phi_registry.get('Nai')(3) == 2

    def gg(x):
        return x

    test_value = 1
    assert gg(test_value) == test_value
    assert phi_registry.get('gg')(test_value) == test_value * 2

    with pytest.raises(registering_phi_at_the_same_key_error):
        PhiFunction.register('')(gg)

    assert phi_registry.get('gg')(test_value) == test_value * 2
