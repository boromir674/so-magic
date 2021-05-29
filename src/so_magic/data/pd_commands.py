"""Defines backend-dependent (eg using pandas as backend library) functions that will serve as engine commands.
These commands should be "built" using a suitable function/decorator.
These commands should be able to be defined at runtime, as part of client code (with respect to this library).
"""
from functools import reduce
import numpy as np
import pandas as pd

from so_magic.data.encoding import NominalAttributeEncoder


__all__ = ['data_manager_commands', 'arbitrary_commands']


# CMD 1
def observations_command(file_path):
    return pd.read_json(file_path, lines=True)


class OneHotEncoder(NominalAttributeEncoder):

    def encode(self, *args, **kwargs):
        datapoints = args[0]
        attribute = args[1]
        prefix_separator = '_'
        dataframe = pd.get_dummies(datapoints.observations[attribute], prefix=attribute, prefix_sep='_',
                                   drop_first=False)
        self.values_set = [x.replace(f'{attribute}{prefix_separator}', '') for x in dataframe.columns]
        self.columns = list(dataframe.columns)
        return dataframe


# CMD 2
def one_hot_encoding_command(_data_manager, _datapoints, _attribute):
    dataframe = OneHotEncoder().encode(_datapoints, _attribute)
    # TODO add a add_columns method to the mutator interface
    # replace below with datapoints.mutator.add_columns(...) (similar to the encode_nominal_subsets_command above)
    _data_manager.datapoints.observations = pd.concat([_data_manager.datapoints.observations, dataframe], axis=1)


class OneHotListEncoder(NominalAttributeEncoder):
    binary_transformer = {True: 1.0, False: 0.0}

    def encode(self, *args, **kwargs):
        datapoints = args[0]
        attribute = args[1]
        self.values_set = reduce(lambda i, j: set(i).union(set(j)),
                                 [_ for _ in datapoints.observations[attribute] if isinstance(_, list)])
        self.columns = list(self.values_set)
        return pd.DataFrame([self._yield_vector(datarow, attribute) for index, datarow in datapoints.iterrows()],
                            columns=self.columns)

    def _yield_vector(self, datarow, attribute):
        decision = {True: self._encode, False: self._encode_none}
        return decision[isinstance(datarow[attribute], list)](datarow, attribute)

    def _encode(self, datarow, attribute):
        return [OneHotListEncoder.binary_transformer[column in datarow[attribute]] for column in self.columns]

    def _encode_none(self, _datarow, _attribute):
        return [0.0] * len(self.values_set)


# CMD 3
def one_hot_encoding_list_command(_data_manager, _datapoints, _attribute):
    _data_manager.datapoints.observations[_attribute].fillna(value=np.nan, inplace=True)
    dataframe = OneHotListEncoder().encode(_datapoints, _attribute)
    _data_manager.datapoints.observations = pd.concat([_data_manager.datapoints.observations, dataframe], axis=1)


data_manager_commands = (one_hot_encoding_list_command, one_hot_encoding_command)
arbitrary_commands = (observations_command,)
