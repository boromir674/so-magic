import os
import shutil
import pytest
from random import randint
from green_magic.strainmaster import StrainMaster
from green_magic.strain_dataset import StrainDataset, LoadingInvalidDatasetError
from green_magic.clustering import ClusteringFactory


# CONSTANTS
my_dir = os.path.dirname(os.path.realpath(__file__))
datasets_dir = os.path.join(my_dir, 'dts')
graphs_dir = os.path.join(my_dir, 'graphs')

sample_source_strains = 'sample-strains.jl'

raw_datafile_path = os.path.join(my_dir, sample_source_strains)

# som_master = StrainMaster(datasets_dir, datasets_dir)

dataset_id = 'unittest-dataset'


all_vars = ['type', 'effects', 'medical', 'negatives', 'flavors']
active_vars = ['type', 'effects', 'medical', 'negatives', 'flavors']


@pytest.fixture(scope='module')
def som_master():
    return StrainMaster(datasets_dir=datasets_dir, maps_dir=graphs_dir)


@pytest.fixture
def sample_datapoints(som_master):
    command = som_master.commands_manager.json_line_dataset
    command.append_arg(raw_datafile_path)
    som_master.load_dataset(command)


class TestStrainMaster:

    @classmethod
    def tear_down_class(cls):
        shutil.rmtree(datasets_dir)
        shutil.rmtree(graphs_dir)

    def test_dataset_operations(self, sample_datapoints, som_master):
        # dt = sm.create_strain_dataset(raw_datafile_path, dataset_id)
        # dt.use_variables(active_vars)
        # sm.dt.clean()
        assert len(som_master.dt) == 98
        assert len(som_master.dt.datapoints[0]) == 72
        # assert os.path.isfile(os.path.join(som_master.datasets_dir, '{}-clean.pk'.format(dataset_id)))

    # @pytest.mark.parametrize("dataset_id, length, nb_datapoints, feature_vector_length", [
    #     ("unittest-dataset", 100, 98, 72),
    # ])
    # def test_clean_dataset_loading(self, dataset_file_name, nb_datapoints, feature_vector_length):
    #     sm.load_dataset(dataset_file_name)
    #     assert len(sm.dt) == nb_datapoints
    #     assert len(sm.dt.datapoints[0]) == feature_vector_length

    # def test_invalid_dataset_creation(self):
    #     with pytest.raises(LoadingInvalidDatasetError):
    #         sm.load_dataset("erroneous-dataset-id")

    # def test_dataset_creation(self):
    #     assert isinstance(dt, StrainDataset)
    #     assert sorted(list(active_vars)) == sorted(list(dt.active_variables))
    #     assert not dt.has_missing_values
    #     assert len(dt.full_df.columns) == len(active_vars)
    #     # self.assertCountEqual(active_vars, self.wm.dt.active_variables)  # a and b have the same elements in the same number, regardless of their order
    #     # self.assertFalse(self.wm.dt.has_missing_values)  # bool(x) is False
    #     # self.assertEqual(len(self.wm.dt.full_df.columns), len(active_vars))
    #     print(len(sm.dt))
    #     assert len(sm.dt) == 98
    #     assert len(sm.dt.datapoints[0]) == 72
    #     # self.assertEqual(len(self.wm.dt), 98)
    #     # self.assertEqual(len(self.wm.dt.datapoints[0]), 72)

    @pytest.mark.parametrize("map_type, length, heigth, nb_clusters", [
        ("toroid", 10, 10, 3),
    ])
    def test_som_creation(self, map_type, length, heigth, nb_clusters, strain_master):
        sm = strain_master
        clf = ClusteringFactory(sm)
        sm.set_feature_vectors()
        som = sm.map_manager.get_som('{}.rectangular.{}.{}.random'.format(map_type, length, heigth))
        assert som.bmus.shape[0] == len(sm.dt)
        assert som.codebook.shape == (10, 10, 72)
        # assert som.codebook.shape == (10, 10, len(sm.dt.datapoints[0]))
        assert som.umatrix.shape == (10, 10)
        assert som._map_type == 'toroid'

        clusters = clf.create_clusters(som, 'kmeans', nb_clusters=nb_clusters, vars=all_vars, ngrams=1)
        assert len(clusters) == nb_clusters
        assert sum([len(_) for _ in clusters]) == len(sm.dt)
        # qr = get_model_quality_reporter(sm, dataset_id)
        # qr.measure(clusters, metric='silhouette')
        # qr.measure(clusters, metric='cali-hara')
