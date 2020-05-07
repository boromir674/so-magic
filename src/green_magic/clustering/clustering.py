import attr

@attr.s
class BaseClustering:
    clusters = attr.ib(init=True)
    id = attr.ib(init=True)

    def __iter__(self):
        return iter([(cluster.id, cluster) for cluster in self.clusters])

    def __len__(self):
        return len(self.clusters)

    def __getitem__(self, item):
        return self.clusters[item]


@attr.s
class Clustering(BaseClustering):
    variables = attr.ib(init=True)

    @property
    def active_variables(self):
        return self.variables

    def __iter__(self):
        for cl in self.clusters:
            yield cl

    def __len__(self):
        return len(self.clusters)

    def __getitem__(self, item):
        return self.clusters[item]

    def get_cluster_id(self, member_id):
        for cl in self:
            if member_id in cl.members:
                return cl.id

    def get_closest(self, an_id, n, metric='euclidean'):
        return sorted((map(lambda x: distance(self.id2vec[an_id], x, metric=metric),
                           [_ for _ in self[self.get_cluster_id(an_id)]])), reverse=True)[:n]

    def gen_ids_and_assigned_clusters(self):
        for cl in self:
            for strain_id in cl.gen_ids():
                yield strain_id, cl.id

@attr.s
class ReportingClustering(Clustering):
    """
    An instance of this class encapsulates the behaviour of a clustering; a set of clusters estimated on some data
    """
    def __str__(self):
        pre = 2
        body, max_lens = self._get_rows(threshold=10, prob_precision=pre)
        header = self._get_header(max_lens, pre, [_ for _ in range(len(self))])
        return header + body

    # clusters = attr.ib(init=True, default=[Cluster(clid2members[cl_id], self._av, cl_id) for cl_id in range(len(clid2members))])
    #
    # def __init__(self, clid2members, active_variables, an_id, map_buffer, dataset_id, fact_ref):
    #     """
    #     :param clid2members: mapping of cluster numerical ids to sets of strain ids
    #     :type clid2members: dict
    #     :param active_variables: the variables taken into account for cl the data
    #     :type active_variables: tuple
    #     :param an_id: a unique identifier for the Clustering object
    #     :type an_id: str
    #     :param map_buffer: a string that can be directly printed showing the topology of the clusters
    #     :type map_buffer: str
    #     :param fact_ref:
    #     :type fact_ref: ClusteringFactory
    # #     """
    #     self._av = active_variables
    #     self.clusters = [Cluster(clid2members[cl_id], self._av, cl_id) for cl_id in range(len(clid2members))]
    #     self.id = an_id + ':{}'.format(len(self))
    #     self.map_buffer = map_buffer
    #     self._fct = fact_ref

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

    def compute_stats(self, id2strain, ngrams=1):
        for cl in self.clusters:
            cl.compute_counts(id2strain,,
            cl.compute_tfs(id2strain)

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



@attr.s
class ClusterFactory:
    pass


@attr.s
class BaseClustering:
    clusters = attr.ib(init=True)



def distance(vec1, vec2, metric='euclidean'):
    return DistanceMetric.get_metric(metric).pairwise([vec1, vec2])[0][1]

@attr.s
class ClusteringFactory(object):
    _sm = attr.ib(init=True)
    algorithms = attr.ib(init=True)


class ClusteringFactory1(object):

    def __init__(self, strain_master):
        self._sm = strain_master
        self.algorithms = {
            'kmeans': lambda x, y: KMeans(n_clusters=x, random_state=y),
            'affinity-propagation': lambda x, y: AffinityPropagation()
        }

    def get_grouping(self, members, active_vars):
        """Uses the currently selected strain dataset id in the strainmaster"""
        gr = Grouping(members, active_vars)
        gr.compute_counts(self._sm.dt.full_df.loc,,
        gr.compute_tfs(self._sm.dt.full_df.loc)
        return gr

    def create_clusters(self, som, algorithm, nb_clusters=8, ngrams=1, random_state=None, vars=None):
        """
        :param som:
        :type som: somoclu.train.Somoclu
        :param algorithm:
        :type algorithm: str
        :param nb_clusters:
        :type nb_clusters: int
        :param ngrams: the degree of ngrams to extract out of ids
        :type ngrams: int
        :param random_state:
        :type random_state: int
        :return:
        :rtype: Clustering
        """
        id2members = {}  # cluster id => members set mapping
        map_id = self._sm.map_manager.map_obj2id[som]
        dt_id = _extract_dataset_id(map_id)
        if vars is None:
            vars = tuple((var for var in self._sm._id2dataset[dt_id].generate_variables()))
        if isinstance(som, Somoclu):
            som.cluster(algorithm=self.algorithms[algorithm](nb_clusters, random_state))
            for i, arr in enumerate(som.bmus):  # iterate through the array of shape [nb_datapoints, 2]. Each row is the coordinates of the neuron the datapoint gets attributed to (closest distance)
                attributed_cluster = som.clusters[arr[0], arr[1]]  # >= 0
                if attributed_cluster not in id2members:
                    id2members[attributed_cluster] = set()
                id2members[attributed_cluster].add(self._sm._id2dataset[dt_id].datapoint_index2_id[i])
        else:
            raise Exception("Clustering is not supported for Self Organizing Map of type '{}'".format(type(som)))
        b = ''
        max_len = len(str(np.max(som.clusters)))  # i.e. an clustering of 11 clusters with ids 0, 1, .., 10 has a max_len = 2
        for j in range(som.umatrix.shape[0]):
            b += ' '.join(' '*(max_len-len(str(i))) + str(i) for i in som.clusters[j, :]) + '\n'
        clustering = Clustering(id2members, vars, map_id, b, dt_id, self)
        clustering.compute_stats(self._sm._id2dataset[dt_id].full_df.loc, ngrams=ngrams)
        print('Created {} clusters with {}'.format(len(clustering), algorithm))
        return clustering


def _extract_dataset_id(map_id):
    return map_id.split('_')[1]  # reverse engineers the MapMakerManager.get_map_id
