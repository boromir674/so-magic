from collections import Counter
from collections import OrderedDict
import numpy as np
from sklearn.neighbors import DistanceMetric
from sklearn.cluster import KMeans, AffinityPropagation
from somoclu import Somoclu

from green_magic.features import enctype2features
from green_magic.utils import extract_value, gen_values, generate_id_tokens


class Clustering(object):
    """
    An instance of this class encapsulates the behaviour of a clustering; a set of clusters estimated on some data
    """
    def __init__(self, clid2members, active_variables, an_id, map_buffer, dataset_id, fact_ref):
        """
        :param clid2members: mapping of cluster numerical ids to sets of strain ids
        :type clid2members: dict
        :param active_variables: the variables taken into account for cl the data
        :type active_variables: tuple
        :param an_id: a unique identifier for the Clustering object
        :type an_id: str
        :param map_buffer: a string that can be directly printed showing the topology of the clusters
        :type map_buffer: str
        :param fact_ref:
        :type fact_ref: ClusteringFactory
        """
        self._av = active_variables
        self.clusters = [Cluster(cl_id, clid2members[cl_id], self._av) for cl_id in range(len(clid2members))]
        self.id = an_id + ':{}'.format(len(self))
        self.map_buffer = map_buffer
        self._fct = fact_ref

    @property
    def active_variables(self):
        return self._av

    @property
    def factory(self):
        return self._fct

    def __str__(self):
        pre = 2
        body, max_lens = self._get_rows(threshold=10, prob_precision=pre)
        header = self._get_header(max_lens, pre, [_ for _ in range(len(self))])
        return header + body

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
        return sorted((map(lambda x: distance(self.id2vec[an_id], x, metric=metric), [_ for _ in self[self.get_cluster_id(an_id)]])), reverse=True)[:n]

    def gen_ids_and_assigned_clusters(self):
        for cl in self:
            for strain_id in cl.gen_ids():
                yield strain_id, cl.id

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
            cl.compute_distros(id2strain)
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
        return ' - '.join('id:{} len:{}'.format(cl.id, len(cl)) + ' ' * (prec + max_lens[i] - len(str(len(cl))) - 6) for i, cl in enumerate(self.gen_clusters(selected_clusters))) + '\n'

    def _get_rows(self, threshold=10, prob_precision=3):
        max_token_lens = [max(map(lambda x: len(x[0]), cl.grams.most_common(threshold))) for cl in self.clusters]
        b = ''
        for i in range(threshold):
            b += ' | '.join('{} '.format(cl.grams.most_common(threshold)[i][0]) + ' '*(max_token_lens[j] - len(cl.grams.most_common(threshold)[i][0])) +
                            "{1:.{0}f}".format(prob_precision, cl.grams.most_common(threshold)[i][1] / len(cl)) for j, cl in enumerate(self.clusters)) + '\n'
        return b, max_token_lens


class Grouping(object):
    def __init__(self, members, active_variables):
        self.members = tuple(members)
        self.vars = active_variables
        self.freqs = OrderedDict()
        self.id_grams = None
        self._bytes = ''

    def __str__(self):
        return 'len {}\n[{}]'.format(len(self), ', '.join((_ for _ in self.gen_ids())))

    def __len__(self):
        return len(self.members)

    def __iter__(self):
        for _id in self.members:
            yield _id

    def gen_ids(self):
        """Iterate with alphabetical order"""
        for _id in sorted((s_id for s_id in self.members), reverse=False):
            yield _id

    def compute_distros(self, id2strain):
        """
        This method calculates
        :param id2strain:
        :return:
        """
        counts = compute_counts(tuple(_ for _ in self.gen_ids()), id2strain, self.vars)
        for var, value_counts in counts.items():
            norm = float(sum(value_counts.values()))
            self.freqs[var] = {k: v / norm for k, v in value_counts.items()}

    def compute_tfs(self, id2strain, field='_id'):
        self.id_grams = Counter()
        for i, text in enumerate((extract_value(id2strain[iid], field) for iid in self.gen_ids())):
            self.id_grams += Counter(generate_id_tokens(text))


class Cluster(Grouping):
    """
    An instance of this class encapsuates the behaviour of a single cluster estimated on some data. The object contains
    essential a "list" of the string ids ponting to unique datapoints.
    """
    def __init__(self, _id, members, active_variables):
        super().__init__(members, active_variables)
        self.id = _id

    def __str__(self):
        return 'cluster id {}, {}'.format(self.id, super().__str__())

    def __next__(self):
        for strain_id in self.gen_ids():
            yield strain_id


def _make_counter_munchable(data, var):
    if var in enctype2features['binary-1'] or var in enctype2features['binary-on-off']:
        return [_ for _ in data]
    elif var in enctype2features['set-real-value']:
        return {k: v for k, v in data}


def compute_counts(iterable_of_ids, id2strain, variables):
    """
    This method calculates count statistics, based on the values of the variables carried by the input strain ids.\n
    :param iterable_of_ids: the collection of ids to compuite stats on (i.e. ('og-kush', 'silver') )
    :type iterable_of_ids: iterable
    :param id2strain:
    :type id2strain: dict
    :param variables:
    :type variables: iterable
    :return: the computed count statistics for the input strain id 'collection'
    :rtype: collections.OrderedDict
    """
    counts = OrderedDict(zip(variables, (Counter() for _ in variables)))
    for iid in iterable_of_ids:
        for var in variables:
            counts[var].update(_make_counter_munchable([_ for _ in gen_values(extract_value(id2strain[iid], var))], var))
    return counts


# def gen_ngrams(text, n=1, normalizer='', word_filter='stopwords'):
#     """
#     This method creates and returns a generator of ngrams based on the input text, a normalizer and potentially a stopwords list.\n
#     :param text: the raw unprocessed text
#     :type text: str
#     :param n: the degree of the id_grams desired to generate
#     :type n: int
#     :param normalizer:
#     :type normalizer: str
#     :param word_filter:
#     :return:
#     """
#     if n == 1:
#         return ('_'.join((_ for _ in gr)) for gr in nltk_ngrams(generate_id_tokens(text), n))
#     else:
#         return ('_'.join((_ for _ in gr)) for gr in nltk_ngrams(generate_tokens_with_padding(text, normalizer=normalizer, word_filter=word_filter), n))


def distance(vec1, vec2, metric='euclidean'):
    return DistanceMetric.get_metric(metric).pairwise([vec1, vec2])[0][1]


class ClusteringFactory(object):

    def __init__(self, strain_master):
        self._sm = strain_master
        self.algorithms = {
            'kmeans': lambda x, y: KMeans(n_clusters=x, random_state=y),
            'affinity-propagation': lambda x, y: AffinityPropagation()
        }

    def get_grouping(self, members, active_vars):
        """Uses the currently selected strain dataset id in the strainmaster"""
        gr = Grouping(members, active_vars)
        gr.compute_distros(self._sm.dt.full_df.loc)
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

