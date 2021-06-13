import pytest


@pytest.fixture
def dataset_without_feature_vectors(somagic, test_datapoints):
    return somagic.dataset


@pytest.fixture
def som_factory_infra():
    from so_magic.som.factory import SelfOrganizingMapFactory
    from so_magic.som.self_organising_map import NoFeatureVectorsError
    return {
        'factory_method': SelfOrganizingMapFactory().create,
        'no_feature_vectors_error': NoFeatureVectorsError
    }


def test_create_method(dataset_without_feature_vectors, som_factory_infra):
    with pytest.raises(som_factory_infra['no_feature_vectors_error'],
                       match='Attempted to train a Som model, but did not find feature vectors in the dataset.'):
        som_factory_infra['factory_method'](dataset_without_feature_vectors, 5, 4)
