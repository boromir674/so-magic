import pytest


@pytest.fixture
def registry_infra():
    from so_magic.utils import ObjectRegistry, ObjectRegistryError
    return type('DummyClass', (object,), {'object': ObjectRegistry({'key1': 1}), 'error': ObjectRegistryError,
                                          'existing_key': 'key1', 'non_existing_key': 'key2'})


def test_sanity_check(registry_infra):
    runtime_repr = repr(registry_infra.object)
    assert runtime_repr == repr(registry_infra.object.objects)
    assert runtime_repr == '{' + ', '.join(f"'{k}': {v}" for k, v in registry_infra.object.objects.items()) + '}'
    assert list(iter(registry_infra.object)) == list(iter(registry_infra.object.objects.items()))


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


@pytest.mark.parametrize('item_value', [9])
def test_add_item_with_existing_key(item_value, registry_infra):
    assert registry_infra.existing_key in registry_infra.object

    with pytest.raises(registry_infra.error, match=f"Requested to insert value '{item_value}' in already existing key "
                                                   f"'{registry_infra.existing_key}'. All keys are "
                                                   rf"\[{', '.join(_ for _ in registry_infra.object.objects)}\]"
                       ):
        registry_infra.object.add(registry_infra.existing_key, item_value)
