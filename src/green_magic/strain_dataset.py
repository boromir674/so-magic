import sys
import json
import pickle
from collections import Counter
from collections import OrderedDict as od
import pandas as pd
from .utils import extract_value
from .definitions import all_vars
from .features import FeatureComputer
import logging
_log = logging.getLogger(__name__)

attributes = ('effects', 'medical', 'negatives')
grow_info = ('difficulty', 'height', 'yield', 'flowering', 'stretch')


class StrainDataset:

    def __str__(self):
        incomplete = self.get_nb_missing('any')
        b = 'Strains dataset: {}\n Active variables: [{}]\n'.format(self.name, ', '.join(_ for _ in self.generate_variables()))
        b += 'Total datapoints: {},'.format(len(self))
        try:
            s = 0
            b += ' with encoded vector length: {}\n'.format(len(self.datapoints[0]))
            for var in self.generate_variables():
                b += ' {}: {} +'.format(var[:5], str(self.get_nb_values(var)))
                s += self.get_nb_values(var)
            b = b[:-1] + '= {}\n'.format(s)
        except IndexError:
            _log.info("Feature space dim has not been established yet. Please call 'self.load_feature_vectors()'")
        b += ' incomplete datapoints: {}\n'.format(incomplete)
        if incomplete != 0:
            b += '\n'.join('  empty \'' + var + '\' vals: ' + str(self.get_nb_missing(var)) for var in self.generate_variables())
        return b

    def __init__(self, a_name):
        self.full_df = pd.DataFrame(columns=all_vars)
        self.name = a_name
        self.active_variables = set()
        self.datapoints = []
        self.datapoint_index2_id = {}
        self.id2datapoint = {}
        self.id2index = {}
        self.linear_index = 0
        self.field2id = dict(zip(all_vars, ({} for _ in all_vars)))  # i.e. field2id['flavors']['mango']
        self.id2field = dict(zip(all_vars, ({} for _ in all_vars)))  # i.e. id2field['flavors'][0]
        self.value_sets = dict(zip(all_vars, (set() for _ in all_vars)))
        self.stats = od.fromkeys(all_vars)
        for k in self.stats.keys():
            self.stats[k] = Counter()
        self.feature_computer = None

    def __getitem__(self, _id):
        if _id not in self.full_df.index:
            raise MissingStrainRequestError("Requested: '{}'; not in dataset with id '{}' that indexes the following strains: [{}]".format(_id, self.name, ', '.join(sorted(list(self.full_df.index)))))
        return self.full_df.loc[_id]

    def __len__(self):
        return len(self.full_df)

    @property
    def has_missing_values(self):
        return self.get_nb_missing('any') != 0

    def add(self, item):
        self.full_df = self.full_df.append(item, ignore_index=True)
        self.id2index[item['_id']] = self.linear_index
        self.linear_index += 1
        self.value_sets['type'].add(str(item['type']))
        if 'flavors' in item:
            for fl in item['flavors']:
                self.value_sets['flavors'].add(str(fl))
                self.stats['flavors'][str(fl)] += 1
        for attr in attributes:
            for key in item[attr].keys():
                self.value_sets[attr].add(str(key))
                self.stats[attr][str(key)] += item[attr][key]
        for gr_inf in grow_info:
            if gr_inf in item['grow_info']:
                self.value_sets[gr_inf].add(str(item['grow_info'][gr_inf]))
                self.stats[gr_inf][str(item['grow_info'][gr_inf])] += 1

    def load_feature_vectors(self):
        self.feature_computer = FeatureComputer(self)
        self.datapoints = []
        self.datapoint_index2_id = {}
        self.id2datapoint = {}
        for index, strain in self.full_df.iterrows():
            datapoint = self.feature_computer.get_basic_feature_representation(strain)
            self.datapoints.append(datapoint)
            self.datapoint_index2_id[len(self.datapoints) - 1] = strain.name
            self.id2datapoint[strain.name] = datapoint
        _log.info("Computed '{}' strain datapoints.".format(len(self.datapoints)))
        return self.datapoints

    def load_feature_indexes(self):
        self.field2id = dict(zip(all_vars, (dict(zip(get_generator(self.value_sets[var]), (num_id for num_id in range(len(self.value_sets[var]))))) for var in all_vars)))
        self.id2field = dict(zip(all_vars, ({v: k for k, v in self.field2id[var].items()} for var in all_vars)))

    def get_nb_values(self, variable):
        """
        Returns the number of distinct and discrete values a data variable can "take". Eg get_nb_values('type') == 3 because set('indica', 'hybrid', 'sativa')
         and also get_nb_values('negative') == 6 despite 'negative' variables hold real numbers. 'negative' has 6 discrete subcategories that take real values\n
        :param variable: the variable name of interest
        :type variable: str
        :return: the number of distinct values
        :rtype: int
        """
        return len(self.value_sets[variable])

    def use_variables(self, list_of_variables):
        """
        :param list_of_variables:
        :return:
        """
        self.active_variables = set(list_of_variables)
        self.full_df = self.full_df[list_of_variables + ['_id']]

    def clean(self):
        self.full_df = self.full_df.dropna()
        self.full_df = self.full_df.set_index('_id')

    def get_nb_missing(self, field):
        if field == 'any':
            return len(self.full_df[self.full_df.isnull().any(axis=1)])
        else:
            return self.full_df[field].isnull().sum()

    def generate_var_value_pairs(self, strain):
        for var in all_vars:
            if var in self.active_variables:
                if var in grow_info:
                    yield var, strain['grow_info'][var]
                else:
                    yield var, strain[var]

    def generate_variables(self):
        for var in all_vars:
            if var in self.active_variables:
                yield var


def get_generator(iterable):
    return (_ for _ in sorted(iterable, reverse=False))


def create_dataset_from_pickle(a_file):
    try:
        with open(a_file, 'rb') as pickle_file:
            strain_dataset = pickle.load(pickle_file)
            assert isinstance(strain_dataset, StrainDataset)
    except FileNotFoundError as e:
        raise LoadingInvalidDatasetError(str(e))
    return strain_dataset


class LoadingInvalidDatasetError(Exception): pass
class MissingStrainRequestError(Exception): pass