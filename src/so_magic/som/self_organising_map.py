import logging
import attr
import numpy as np
import somoclu
from sklearn.cluster import KMeans

logger = logging.getLogger(__name__)


def infer_map(nb_cols, nb_rows, dataset, **kwargs):
    """Infer a self-organizing map from dataset.\n
    initialcodebook = None, kerneltype = 0, maptype = 'planar', gridtype = 'rectangular',
    compactsupport = False, neighborhood = 'gaussian', std_coeff = 0.5, initialization = None
    """
    if not hasattr(dataset, 'feature_vectors'):
        raise NoFeatureVectorsError("Attempted to train a Som model, "
                                    "but did not find feature vectors in the dataset.")
    som = somoclu.Somoclu(nb_cols, nb_rows, **kwargs)
    som.train(data=np.array(dataset.feature_vectors, dtype=np.float32))
    return som


@attr.s(slots=True)
class SomTrainer:
    infer_map: callable = attr.ib()

    @staticmethod
    def from_callable():
        return SomTrainer(infer_map)


@attr.s
class SelfOrganizingMap:
    som = attr.ib(init=True)
    dataset_name = attr.ib(init=True)

    @property
    def height(self):
        return self.som._n_rows

    @property
    def width(self):
        return self.som._n_columns

    @property
    def type(self):
        return self.som._map_type

    @property
    def grid_type(self):
        return self.som._grid_type

    def __getattr__(self, item):
        if item in ('n_rows', 'n_columns', 'initialization', 'map_type', 'grid_type'):
            item = f'_{item}'
        return getattr(self.som, item)

    def get_map_id(self):
        _ = '_'.join(getattr(self, attribute) for attribute in
                     ['dataset_name', 'n_rows', 'n_columns', 'initialization', 'map_type', 'grid_type'])
        if self.som.clusters:
            return f'{_}_cl{self.nb_clusters}'
        return _

    @property
    def nb_clusters(self):
        return np.max(self.som.clusters)

    def neurons_coordinates(self):
        raise NotImplementedError
        # # iterate through the array of shape [nb_datapoints, 2]. Each row is the coordinates
        # for i, arr in enumerate(self.som.bmus):
        #     # of the neuron the datapoint gets attributed to (closest distance)
        #     attributed_cluster = self.som.clusters[arr[0], arr[1]]  # >= 0
        #     id2members[attributed_cluster].add(dataset[i].id)

    def datapoint_coordinates(self, index):
        """Get the best-matching unit (bmu) coordinates of the datapoint indexed by the input pointer.\n

        Bmu is simply the neuron on the som grid that is closest to the projected-into-2D-space datapoint."""
        return self.som.bmus[index][0], self.som.bmus[index][1]

    def project(self, datapoint):
        """Compute the coordinates of a (potentially unseen) datapoint.

        It is assumed that the codebook has been computed already."""
        raise NotImplementedError

    def cluster(self, nb_clusters, random_state=None):
        self.som.cluster(algorithm=KMeans(n_clusters=nb_clusters, random_state=random_state))

    @property
    def visual_umatrix(self):
        buffer = ''
        # i.e. a clustering of 11 clusters with ids 0, 1, .., 10 has a max_len = 2
        max_len = len(str(np.max(self.som.clusters)))
        for j in range(self.som.umatrix.shape[0]):
            buffer += ' '.join(' ' * (max_len - len(str(i))) + str(i) for i in self.som.clusters[j, :]) + '\n'
        return buffer


class NoFeatureVectorsError(Exception): pass
