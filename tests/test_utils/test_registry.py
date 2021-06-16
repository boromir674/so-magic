import pytest


@pytest.fixture
def registry_infra():
    from so_magic.utils import ObjectRegistry, ObjectRegistryError
    return type('DummyClass', (object,), {'object': ObjectRegistry({'key1': 1}), 'error': ObjectRegistryError})


def test_registry_remove_method(registry_infra):
    key_to_remove = 'key1'
    assert key_to_remove in registry_infra.object

    registry_infra.object.remove(key_to_remove)
    assert registry_infra.object.objects == {}

    with pytest.raises(registry_infra.error,
                       match=f'Requested to remove item with key {key_to_remove}, which does not exist.'):
        registry_infra.object.remove(key_to_remove)
    

def test_registry_pop_method(registry_infra):
    key_to_pop = 'key1'
    assert key_to_pop in registry_infra.object

    value = registry_infra.object.pop(key_to_pop)
    assert value == 1
    assert registry_infra.object.objects == {}

    with pytest.raises(registry_infra.error,
                       match=f'Requested to pop item with key {key_to_pop}, which does not exist.'):
        registry_infra.object.pop(key_to_pop)


def test_registry_get_method(registry_infra):
    key_to_get = 'key1'
    assert key_to_get in registry_infra.object

    value = registry_infra.object.get(key_to_get)
    assert value == 1
    assert registry_infra.object.objects == {'key1': 1}

    non_existing_key = 'key2'
    with pytest.raises(registry_infra.error,
                       match=f'Requested to get item with key {non_existing_key}, which does not exist.'):
        _ = registry_infra.object.get(non_existing_key)
