import numpy as np


class DistroReporter(object):

    def __init__(self):
        self.cl = None
        self.var = ''
        self.sl = None

        self.ordered_value_labels = []
        self.max_nb_rows = 0
        self.max_label_len = 0
        self.generators = []

    def print_distros(self, clustering, variable, selected_clusters='all', prec=3):
        """
        Prints the discrete distribution of the values the input variable takes for evry selected cluster. Frequencies are shown in descending order.\n
        :param clustering: the Clustering to select from
        :type clustering: clustering.Cluster
        :param variable: the field name of interest
        :type variable: str
        :param selected_clusters: can be a list of indices pointing to Cluster objects in the Clustering structure. Can take the 'all' value to indicate selecting every cluster
        :type selected_clusters: list or str
        :param prec: the precision of the frequencies to visualize; the number of decimal digits to show
        :type prec: int
        """
        self._set_state(clustering, variable, selected_clusters, prec)
        body = ''
        for i in range(self.max_nb_rows):
            body += ' | '.join(str(self.generators[j].__next__()) for j in range(len(self.sl))) + '\n'
        header = ' - '.join('id:{} len:{}'.format(cl.id, len(cl)) + ' '*(prec + self.max_label_len[i] - len(str(len(cl))) - 6) for i, cl in enumerate(self.cl.gen_clusters(self.sl))) + '\n'
        print(header + body)

    def _set_state(self, clustering, variable, selected_clusters, prec):
        self.cl = clustering
        self.var = variable
        if selected_clusters == 'all':
            selected_clusters = range(len(self.cl))
        self.sl = selected_clusters
        self.ordered_value_labels = [sorted(cl.freqs[self.var], key=lambda x: cl.freqs[self.var][x], reverse=True) for cl in self.cl.gen_clusters(self.sl)]
        self.max_nb_rows = max(map(lambda x: len(x), self.ordered_value_labels))
        self.max_label_len = [max(map(lambda x: len(x), cl.freqs[variable])) for cl in self.cl.gen_clusters(self.sl)]
        self.generators = [self._get_generator(i, prec) for i in range(len(self.sl))]

    def _gen_entries(self, ind, prec):
        i = 0
        for i, el in enumerate(self.ordered_value_labels[ind]):
            yield '{0} {1}{3:.{2}f}'.format(el, ' '*(self.max_label_len[ind] - len(el)), prec, self.cl[self.sl[ind]].freqs[self.var][el])
        while i < self.max_nb_rows - 1:
            yield ' ' * (self.max_label_len[ind] + prec + 3)
            i += 1

    def _get_generator(self, ind, prec):
        return (_ for _ in self._gen_entries(ind, prec))
