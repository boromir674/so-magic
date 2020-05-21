import attr
import numpy as np
import somoclu
from sklearn.cluster import KMeans


@attr.s
class SomTrainer:

    def train_map(self, nb_cols, nb_rows, dataset, **kwargs):
        """Infer a self-organizing map from dataset.\n
        initialcodebook = None, kerneltype = 0, maptype = 'planar', gridtype = 'rectangular',
        compactsupport = False, neighborhood = 'gaussian', std_coeff = 0.5, initialization = None
        """
        if not dataset.datapoints.vectors:
            raise NoFeatureVectorsError("Attempted to train a Som model, but did not find feature vectors in the dataset.")
        som = somoclu.Somoclu(nb_cols, nb_rows, **kwargs)
        som.train(data=np.array(dataset.datapoints, dtype=np.float32))
        return som

class NoFeatureVectorsError(Exception): pass


@attr.s
class SOMFacade:
    som = attr.ib(init=True)

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
    def bmus(self):
        return self.som.bmus
    @property
    def clusters(self):
        return self.som.clusters
    @property
    def visual_umatrix(self):
        b = ''
        max_len = len(str(np.max(self.som.clusters)))  # i.e. a clustering of 11 clusters with ids 0, 1, .., 10 has a max_len = 2
        for j in range(self.som.umatrix.shape[0]):
            b += ' '.join(' ' * (max_len - len(str(i))) + str(i) for i in self.som.clusters[j, :]) + '\n'
        return b
