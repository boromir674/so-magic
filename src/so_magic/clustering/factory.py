from .clustering import ReportingClustering
from .cluster import SOMCluster

import attr

@attr.s
class ClusteringFactory(object):
    # algorithms = attr.ib(init=True)

    @classmethod
    def inferred(cls, x):
        pass

    def from_som(self, dataset, som, nb_clusters, **kwargs):  #  algorithm, nb_clusters=8, ngrams=1, random_state=None, vars=None):
        id2members = dict.fromkeys(range(nb_clusters), set())  # cluster id => members set mapping
        som.cluster(nb_clusters, random_state=kwargs.get('random_state', None))
        # som.cluster(algorithm=self.algorithms[algorithm](nb_clusters, kwargs.get('random_state', None)))
        for i, arr in enumerate(som.bmus):  # iterate through the array of shape [nb_datapoints, 2]. Each row is the coordinates
            # of the neuron the datapoint gets attributed to (closest distance)
            attributed_cluster = som.clusters[arr[0], arr[1]]  # >= 0
            id2members[attributed_cluster].add(dataset.datapoints[i])
        def ex1(a_cluster):
            return [_ for _ in a_cluster]
        def ex2(datapoints, attribute):
            return datapoints[str(attribute)]

        return ReportingClustering([SOMCluster(cluster_members) for cluster_members in id2members.values()],
                                   str(dataset)+'-'+str(som),
                                   ex1,
                                   ex2,
                                   )
