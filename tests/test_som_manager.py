import pytest


@pytest.fixture
def map_manager(somagic):
    return somagic.map.manager


@pytest.fixture
def map_id_class():
    from so_magic.som.manager import MapId
    return MapId


@pytest.fixture
def identical_map_ids():
    def assert_map_ids_are_the_same(map_id1, map_id2):
        assert str(map_id1) == str(map_id2)
        assert dict(map_id1) == dict(map_id2)
    return assert_map_ids_are_the_same


def test_map_manager_get_map_method(map_manager, test_dataset, map_id_class, identical_map_ids):
    # assert the get_map method returns the same object when invoked with already seen arguments
    som1 = map_manager.get_map(test_dataset, 4, 5, initialization='pca', maptype='toroid', gridtype='hexagonal')
    som2 = map_manager.get_map(test_dataset, 4, 5, initialization='pca', maptype='toroid', gridtype='hexagonal')
    assert id(som1) == id(som2)

    map_id = map_id_class.from_self_organizing_map(som1)
    identical_map_ids(map_id, map_id_class(
        test_dataset.name,
        4,
        5,
        'pca',
        'toroid',
        'hexagonal'
    ))

    assert som1.get_map_id() == str(map_id)
    assert som1.nb_clusters == 0

    with pytest.raises(TypeError, match="'NoneType' object is not subscriptable"):
        _ = som1.visual_umatrix

    # tightly depends on the current implementation that requires to invoke the
    # 'cluster' method of a SelfOrganisingMap instance to do 'clustering' on the
    # output of the self-organising map training/learning algorithm
    som1.cluster(4, random_state=1)
    assert som1.nb_clusters == 4

    umatrix_str_representation = som1.visual_umatrix

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

    assert som1.datapoint_coordinates(0) == (2, 1)
