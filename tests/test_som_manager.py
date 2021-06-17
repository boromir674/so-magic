import pytest


@pytest.fixture
def map_manager(somagic):
    return somagic.map.manager


@pytest.fixture
def test_data(test_dataset):
    from collections import OrderedDict
    from so_magic.som.manager import MapId
    map_specs = OrderedDict([
        ('nb-cols', 4),
        ('nb-rows', 5),
        ('initialization', 'pca'),
        ('maptype', 'toroid'),
        ('gridtype', 'hexagonal'),
    ])
    return type('TestData', (object,), {
        'map_parameters': type('SomModelParameters', (object,), {
            'args': (test_dataset, map_specs['nb-cols'], map_specs['nb-rows']),
            'kwargs': {k: map_specs[k] for k in ('initialization', 'maptype', 'gridtype')}
        }),
        'get_runtime_map_id': lambda x: MapId.from_self_organizing_map(x),
        'expected_map_id': MapId(*[test_dataset.name] + list(map_specs.values())),
    })


@pytest.fixture
def test_soms(map_manager, test_data):
    som1 = map_manager.get_map(*test_data.map_parameters.args, **test_data.map_parameters.kwargs)
    som2 = map_manager.get_map(*test_data.map_parameters.args, **test_data.map_parameters.kwargs)
    return [som1, som2]


def test_memoize_behaviour(test_soms):
    assert id(test_soms[0]) == id(test_soms[1])


def test_map_id(test_soms, test_data):
    map_id = test_data.get_runtime_map_id(test_soms[0])
    assert str(map_id) == str(test_data.expected_map_id)
    assert dict(map_id) == dict(test_data.expected_map_id)
    assert test_soms[0].get_map_id() == str(map_id)


def test_clustering_behaviour(test_soms):
    assert test_soms[0].nb_clusters == 0

    with pytest.raises(TypeError, match="'NoneType' object is not subscriptable"):
        _ = test_soms[0].visual_umatrix

    # tightly depends on the current implementation that requires to invoke the
    # 'cluster' method of a SelfOrganisingMap instance to do 'clustering' on the
    # output of the self-organising map training/learning algorithm
    test_soms[0].cluster(4, random_state=1)
    assert test_soms[0].nb_clusters == 4

    umatrix_str_representation = test_soms[0].visual_umatrix

    assert umatrix_str_representation == '3 3 3 3\n2 0 0 0\n2 2 0 0\n1 1 1 1\n1 1 1 1\n'
    assert umatrix_str_representation == '3 3 3 3\n' \
                                         '2 0 0 0\n' \
                                         '2 2 0 0\n' \
                                         '1 1 1 1\n' \
                                         '1 1 1 1\n'
    assert umatrix_str_representation == '\
3 3 3 3\n\
2 0 0 0\n\
2 2 0 0\n\
1 1 1 1\n\
1 1 1 1\n\
'

    assert test_soms[0].datapoint_coordinates(0) == (2, 1)
