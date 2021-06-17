import pytest


@pytest.fixture
def registry_infra():
    from so_magic.utils import ObjectRegistry, ObjectRegistryError
    return type('DummyClass', (object,), {'object': ObjectRegistry({'key1': 1}), 'error': ObjectRegistryError,
                                          'existing_key': 'key1', 'non_existing_key': 'key2'})


def test_registry_remove_method(registry_infra):
    assert registry_infra.existing_key in registry_infra.object

    registry_infra.object.remove(registry_infra.existing_key)
    assert registry_infra.object.objects == {}

    with pytest.raises(registry_infra.error,
                       match=f'Requested to remove item with key {registry_infra.existing_key}, which does not exist.'):
        registry_infra.object.remove(registry_infra.existing_key)


def test_registry_pop_method(registry_infra):
    assert registry_infra.existing_key in registry_infra.object

    value = registry_infra.object.pop(registry_infra.existing_key)
    assert value == 1
    assert registry_infra.object.objects == {}

    with pytest.raises(registry_infra.error,
                       match=f'Requested to pop item with key {registry_infra.existing_key}, which does not exist.'):
        registry_infra.object.pop(registry_infra.existing_key)


def test_registry_get_method(registry_infra):
    assert registry_infra.existing_key in registry_infra.object

    value = registry_infra.object.get(registry_infra.existing_key)
    assert value == 1
    assert registry_infra.object.objects == {registry_infra.existing_key: 1}

    with pytest.raises(registry_infra.error, match=f'Requested to get item with key {registry_infra.non_existing_key}, '
                                                   f'which does not exist.'):
        _ = registry_infra.object.get(registry_infra.non_existing_key)
