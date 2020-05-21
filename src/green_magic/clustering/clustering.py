import attr

from .computing import ClusterDistroComputer

@attr.s
class BaseClustering:
    """Items grouped in clusters/subgroups (eg based on proximity, similarity)"""
    clusters = attr.ib(init=True)
    id = attr.ib(init=True)

    def __iter__(self):
        return iter([(cluster.id, cluster) for cluster in self.clusters])

    def __len__(self):
        return len(self.clusters)

    def __getitem__(self, item):
        return self.clusters[item]

    def members_n_assigned_clusters(self):
        """Generate tuples of cluster members and their assigned cluster index"""
        for i, cl in enumerate(self.clusters):
            for strain_id in iter(cl):
                yield strain_id, i


@attr.s
class DatapointsCluster(BaseClustering):
    """
    Provide a method to return datapoints from a cluster and a method to get the values of all datapoints for a given attribute.
    """
    datapoints_extractor = attr.ib(init=True)  # call(cluster) -> datapoints
    attributes_extractor = attr.ib(init=True)  # call(datapoints, attribute) -> attribute_value per datapoint iterable

    distro_computer = attr.ib(init=False, default=attr.Factory(lambda self: ClusterDistroComputer.from_extractors(
        self.datapoints_extractor, self.attributes_extractor), takes_self=True))
    members = attr.ib(init=False, default={})  # structure to use to cache found items in the clustering, so that we do not seek them next time


@attr.s
class ReportingClustering(DatapointsCluster):
    """
    An instance of this class encapsulates the behaviour of a clustering; a set of clusters estimated on some data
    """

    pre = 2
    def __str__(self):
        body, max_lens = self._get_rows(threshold=10, prob_precision=pre)
        header = self._get_header(max_lens, pre, [_ for _ in range(len(self))])
        return header + body

    def cluster_of(self, item):
        h = hash(item)
        return self.members.get(h, self._find_cluster(h))

    def _find_cluster(self, item):
        """Call this method to seek through the clusters for the given item."""
        for cluster in self:
            if item in cluster.members:
                self.members[item] = cluster.id
                return self.members[item]

    def gen_clusters(self, selected):
        """
        Generates Cluster objects according to the indices in the selected clusters list
        :param selected: the indices of the clusters to select
        :type selected: list
        :return: the generated cluster
        :rtype: Cluster
        """
        for i in selected:
            yield self[i]

    def get_closest(self, an_id, n, metric='euclidean'):
        """Call this method to find n closest vectors (within the same cluster) to the vector corresponding to the input id."""
        return sorted((map(lambda x: distance(self.id2vec[an_id], x, metric=metric),
                           [_ for _ in self[self.find_cluster(an_id)]])), reverse=True)[:n]

    def compute_stats1(self, cluster, attributes):
        self._stats = self.distro_computer(cluster, attributes)

    def print_clusters(self, selected_clusters='all', threshold=10, prec=2):
        if selected_clusters == 'all':
            selected_clusters = range(len(self))
        body, max_lens = self._get_rows(threshold=threshold, prob_precision=prec)
        header = self._get_header(max_lens, prec, selected_clusters)
        # header = ' - '.join('id:{} len:{}'.format(i, len(self[i])) + ' ' * (3-9 + prec + max_lens[i] - len(str(len(self[i])))) for i in selected_clusters) + '\n'
        print(header + body)

    def print_map(self):
        print(self.map_buffer)

    def _get_header(self, max_lens, prec, selected_clusters):
        assert len(max_lens) == len(selected_clusters)
        return ' - '.join(
            'id:{} len:{}'.format(cl.id, len(cl)) + ' ' * (prec + max_lens[i] - len(str(len(cl))) - 6) for i, cl in
            enumerate(self.gen_clusters(selected_clusters))) + '\n'

    def _get_rows(self, threshold=10, prob_precision=3):
        max_token_lens = [max(map(lambda x: len(x[0]), cl.grams.most_common(threshold))) for cl in self.clusters]
        b = ''
        for i in range(threshold):
            b += ' | '.join('{} '.format(cl.grams.most_common(threshold)[i][0]) + ' ' * (
                        max_token_lens[j] - len(cl.grams.most_common(threshold)[i][0])) +
                            "{1:.{0}f}".format(prob_precision, cl.grams.most_common(threshold)[i][1] / len(cl)) for
                            j, cl in enumerate(self.clusters)) + '\n'
        return b, max_token_lens


def distance(vec1, vec2, metric='euclidean'):
    return DistanceMetric.get_metric(metric).pairwise([vec1, vec2])[0][1]
