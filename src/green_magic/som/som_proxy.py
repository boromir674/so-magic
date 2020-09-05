import attr
import numpy as np
import somoclu
from sklearn.cluster import KMeans

import logging
logger = logging.getLogger(__name__)


class SomTrainer:

    def infer_map(self, nb_cols, nb_rows, dataset, **kwargs):
        """Infer a self-organizing map from dataset.\n
        initialcodebook = None, kerneltype = 0, maptype = 'planar', gridtype = 'rectangular',
        compactsupport = False, neighborhood = 'gaussian', std_coeff = 0.5, initialization = None
        """
        if not hasattr(dataset, 'feature_vectors'):
            raise NoFeatureVectorsError("Attempted to train a Som model, but did not find feature vectors in the dataset.")
        som = somoclu.Somoclu(nb_cols, nb_rows, **kwargs)
        som.train(data=np.array(dataset.feature_vectors, dtype=np.float32))
        return som


@attr.s
class SomFactory:
    """Implementing from the BaseSomFactory allows other class to register/subscribe on (emulated) 'events'.
       So, when the factory creates a new Som object, other entities can be notified."""
    trainer = attr.ib(init=True, default=SomTrainer())
    observers = attr.ib(init=False, default=[])

    def register(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def unregister(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def unregister_all(self):
        if self.observers:
            del self.observers[:]

    def update_observers(self, *args, **kwargs):
        for observer in self.observers:
            observer.update(*args, **kwargs)

    def create_som(self, nb_cols, nb_rows, dataset, **kwargs):
        try:
            map_obj = self.trainer.infer_map(nb_cols, nb_rows, dataset, **kwargs)
            self.update_observers(nb_rows, nb_cols, map_object=map_obj)
            return map_obj
        except NoFeatureVectorsError as e:
            logger.info(f"{e}. Fire up an 'encode' command.")
            raise e


class NoFeatureVectorsError(Exception): pass


@attr.s
class SelfOrganizingMapFactory:
    som_factory = attr.ib(init=True, default=SomFactory())

    def create(self, dataset, nb_cols, nb_rows, **kwargs):
        return SelfOrganizingMap(self.som_factory.create_som(nb_cols, nb_rows, dataset, **kwargs), dataset.name)


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
        _ = '_'.join(getattr(self, attribute) for attribute in ['dataset_name', 'n_rows', 'n_columns', 'initialization', 'map_type', 'grid_type'])
        if self.som.clusters:
            return f'{_}_cl{self.nb_clusters}'
        return _

    @property
    def nb_clusters(self):
        return np.max(self.som.clusters)

    def neurons_coordinates(self):
        """"""
        for i, arr in enumerate(self.som.bmus):  # iterate through the array of shape [nb_datapoints, 2]. Each row is the coordinates
            # of the neuron the datapoint gets attributed to (closest distance)
            attributed_cluster = self.som.clusters[arr[0], arr[1]]  # >= 0
            id2members[attributed_cluster].add(dataset[i].id)

    def datapoint_coordinates(self, index):
        """Call this method to get the best-matching unit (bmu) coordinates of the datapoint indexed byt the input pointer.\n
        Bmu is simply the neuron on the som grid that is closest to the datapoint after being projected to the 2D space."""
        return self.som.bmus[index][0], self.som.bmus[index][1]

    def project(self, datapoint):
        """Compute the coordinates of a (potentially unseen) datapoint. It is assumed that the codebook has been computed already."""
        pass

    def cluster(self, nb_clusters, random_state=None):
        som.cluster(algorithm=KMeans(n_clusters=nb_clusters, random_state=random_state))

    @property
    def visual_umatrix(self):
        b = ''
        max_len = len(str(np.max(self.som.clusters)))  # i.e. a clustering of 11 clusters with ids 0, 1, .., 10 has a max_len = 2
        for j in range(self.som.umatrix.shape[0]):
            b += ' '.join(' ' * (max_len - len(str(i))) + str(i) for i in self.som.clusters[j, :]) + '\n'
        return b


