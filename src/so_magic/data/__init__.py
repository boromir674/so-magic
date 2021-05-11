from .data_manager import DataManager
from .features.phi import PhiFunctionRegistrator
from .features import FeatureManager
from .command_factories import DataManagerCommandFactory


def init_data_manager(a_backend):
    data_manager = DataManager(a_backend, type('PhiFunction', (PhiFunctionRegistrator,), {}), FeatureManager([]))
    mega_cmd_factory = DataManagerCommandFactory(data_manager)
    mega_cmd_factory.attach(data_manager.commands_manager.command.accumulator)

    @data_manager.backend.engine.dec()
    def encode_nominal_subsets(datapoints, attribute, new_attribute):
        from so_magic.data.features.phis import ListOfCategoricalPhi, DatapointsAttributePhi
        phi = ListOfCategoricalPhi(DatapointsAttributePhi(datapoints))
        new_values = phi(attribute)
        datapoints.mutator.add_column(datapoints, new_values, new_attribute)

    import pandas as pd

    @data_manager.backend.engine.dec()
    def observations(file_path):
        return pd.read_json(file_path, lines=True)

    from so_magic.data.encoding import NominalAttributeEncoder


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


    @mega_cmd_factory.build_command_prototype()
    def one_hot_encoding(_data_manager, _datapoints, _attribute):
        dataframe = OneHotEncoder().encode(_datapoints, _attribute)
        _data_manager.datapoints.observations = pd.concat([_data_manager.datapoints.observations, dataframe], axis=1)


    @mega_cmd_factory.build_command_prototype()
    def select_variables(_data_manager, variables):
        _data_manager.feature_manager.feature_configuration = variables


    import numpy as np
    from functools import reduce

    class OneHotListEncoder(NominalAttributeEncoder):
        binary_transformer = {True: 1.0, False: 0.0}

        def encode(self, *args, **kwargs):
            datapoints = args[0]
            attribute = args[1]
            self.values_set = reduce(lambda i, j: set(i).union(set(j)),
                                     [_ for _ in datapoints.observations[attribute] if type(_) == list])
            self.columns = [_ for _ in self.values_set]
            return pd.DataFrame([self._yield_vector(datarow, attribute) for index, datarow in datapoints.iterrows()],
                                columns=self.columns)

        def _yield_vector(self, datarow, attribute):
            decision = {True: self._encode, False: self._encode_none}
            return decision[type(datarow[attribute]) == list](datarow, attribute)

        def _encode(self, datarow, attribute):
            return [OneHotListEncoder.binary_transformer[column in datarow[attribute]] for column in self.columns]

        def _encode_none(self, _datarow, _attribute):
            return [0.0] * len(self.values_set)

    @mega_cmd_factory.build_command_prototype()
    def one_hot_encoding_list(_data_manager, _datapoints, _attribute):
        _data_manager.datapoints.observations[_attribute].fillna(value=np.nan, inplace=True)
        dataframe = OneHotListEncoder().encode(_datapoints, _attribute)
        _data_manager.datapoints.observations = pd.concat([_data_manager.datapoints.observations, dataframe],
                                                            axis=1)

    return data_manager
