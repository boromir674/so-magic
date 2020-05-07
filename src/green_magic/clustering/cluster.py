from _collections import Counter, OrderedDict


@attr.s
class Grouping:
    members = attr.ib(init=True, converter=tuple)
    vars = attr.ib(init=True)

    sort = attr.ib(init=False, default={True: sorted, False: lambda x: x})

    def __str__(self):
        return f'len {len(self.members)}'

    def __len__(self):
        return len(self.members)

    def __iter__(self):
        for item in self.members:
            yield item

    def _gen_members(self, **kwargs):
        return iter(self.sort[kwargs.get('sort', False)](self.members, reverse=kwargs.get('reverse', False)))
    def gen_members(self, **kwargs):
        return self._gen_members(**kwargs)
    def alphabetical(self):
        return self._gen_members(sort=True)

@attr.s
class Cluster(Grouping):
    """
    An instance of this class encapsuates the behaviour of a single cluster estimated on some data. The object contains
    essentially a "list" of objects
    """

    def __next__(self):
        for strain_id in self.gen_ids():
            yield strain_id

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
            self.id_grams += Counter(Grouping.generate_id_tokens(text))

    @staticmethod
    def generate_id_tokens(text):
        for id_token in text.split('-'):
            yield id_token

# freqs = attr.ib(init=False, default=OrderedDict)
#     id_grams = attr.ib(init=False, default=None)
#     _bytes = attr.ib(init=True, default='')

from abc import ABC, abstractmethod

class AbstractCountsComputer(ABC):
    @abstractmethod
    def compute_counts(self, cluster, attributes):
        raise NotImplementedError

@attr.s
class BaseCountsComputer(AbstractCountsComputer):
    extractor = attr.ib(init=True)

    def compute_counts(self, cluster, attributes):
        c = {k: Counter() for k in attributes}
        for attribute in attributes:
            c[attribute].update([self.getattr(item, attribute) for item in cluster])
        return c

    @abstractmethod
    def getattr(self, item, attribute):
        return self.extractor(item, attribute)


@attr.s
class DistroComputer:
    cc = attr.ib(init=False)
    freqs = attr.ib(init=False, default={})
    norms = attr.ib(init=False, default={})

    def compute_distros(self, cluster, attributes=None):
        if attributes is None:
            attributes = dir(extractor(cluster[0]))
        counts = cc.compute_counts(cluster, attributes)
        self.freqs =

        for var, value_counts in counts.items():
            norm = float(sum(value_counts.values()))
            self.freqs[var] = {k: v / norm for k, v in value_counts.items()}

    def _set_norms(self, counts):
        self.norms = DistroComputer._norms(counts)


    @classmethod
    def _norms(cls, counts):
        return {attr: float(sum(attr_value_cs.values())) for attr, attr_value_cs in counts.items()}

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


def extract_value(strain, field):
    if field == '_id':
        return strain.name
    if field in grow_info:
        return strain['grow_info'][field]
    else:
        return strain[field]


def _make_counter_munchable(data, var):
    if var in enctype2features['binary-1'] or var in enctype2features['binary-on-off']:
        return [_ for _ in data]
    elif var in enctype2features['set-real-value']:
        return {k: v for k, v in data}


def gen_values(extr_output):
    """
    Expects the content of a strain item's field. In other words the data contained in the specific dataframe column.
    :param extr_output: the content of a strain item's field
    :return: the values contained
    """
    if type(extr_output) == list:
        for i in extr_output:
            yield i
    elif type(extr_output) == str:
        yield extr_output
    else:  # dictionary like
        for k, v in extr_output.items():
            yield k, v
