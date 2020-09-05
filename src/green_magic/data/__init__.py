from .data_manager import DataManager
from .features.phi import PhiFunctionRegistrator
from .features import FeatureManager
from .command_factories import MegaCommandFactory


def init_data_manager(a_backend):
    data_manager = DataManager(a_backend, type('PhiFunction', (PhiFunctionRegistrator,), {}), FeatureManager([]))
    mega_cmd_factory = MegaCommandFactory(data_manager)
    mega_cmd_factory.attach(data_manager.commands_manager.command.accumulator)

    mega_cmd_factory('select_variables')

    @data_manager.backend.engine.dec()
    def encode_nominal_subsets(datapoints, attribute, new_attribute):
        from green_magic.data.features.phis import ListOfCategoricalPhi, DatapointsAttributePhi
        phi = ListOfCategoricalPhi(DatapointsAttributePhi(datapoints))
        new_values = phi(attribute)
        datapoints.mutator.add_column(datapoints, new_values, new_attribute)

    import pandas as pd

    @data_manager.backend.engine.dec()
    def observations(file_path):
        return pd.read_json(file_path, lines=True)

    from green_magic.data.encoding import NominalAttributeEncoder

    @NominalAttributeEncoder.register_as_subclass('one_hot')
    class OneHotEncoder(NominalAttributeEncoder):

        def encode(self, *args, **kwargs):
            datapoints = args[0]
            attribute = args[1]
            prefix_separator = '_'
            dataframe = pd.get_dummies(datapoints.observations[attribute], prefix=attribute, prefix_sep='_', drop_first=False)
            self.values_set = [x.replace(f'{attribute}{prefix_separator}', '') for x in dataframe.columns]
            self.columns = [x for x in dataframe.columns]
            return dataframe

    from green_magic.data.command_factories import DataManagerCommandFactory
    from green_magic.utils import Command

    @DataManagerCommandFactory.register_as_subclass('one_hot_encoding')
    class EncodeNominalCommandFactory(DataManagerCommandFactory):

        def construct(self, *args, **kwargs) -> Command:
            _data_manager= args[0]
            def one_hot_encoding(_datapoints, _attribute):
                dataframe = OneHotEncoder().encode(_datapoints, _attribute)
                _data_manager.datapoints.observations = pd.concat([_data_manager.datapoints.observations, dataframe], axis=1)
            return Command(one_hot_encoding, '__call__', *args[1:])

    mega_cmd_factory('one_hot_encoding')

    import numpy as np
    from functools import reduce

    @NominalAttributeEncoder.register_as_subclass('one_hot_list')
    class OneHotListEncoder(NominalAttributeEncoder):
        binary_transformer = {True: 1.0, False: 0.0}

        def encode(self, *args, **kwargs):
            datapoints = args[0]
            attribute = args[1]
            self.values_set = reduce(lambda i, j: set(i).union(set(j)), [_ for _ in datapoints.observations[attribute] if type(_) == list])
            self.columns = [_ for _ in self.values_set]
            return pd.DataFrame([self._yield_vector(datarow, attribute) for index, datarow in datapoints.iterrows()], columns=self.columns)

        def _yield_vector(self, datarow, attribute):
            decision = {True: self._encode, False: self._encode_none}
            return decision[type(datarow[attribute]) == list](datarow, attribute)

        def _encode(self, datarow, attribute):
            return [OneHotListEncoder.binary_transformer[column in datarow[attribute]] for column in self.columns]

        def _encode_none(self, datarow, attribute):
            return [0.0] * len(self.values_set)


    @DataManagerCommandFactory.register_as_subclass('one_hot_encoding_list')
    class EncodeNominalListCommandFactory(DataManagerCommandFactory):

        def construct(self, *args, **kwargs) -> Command:
            _data_manager = args[0]

            def one_hot_encoding_list(_datapoints, _attribute):
                _data_manager.datapoints.observations[_attribute].fillna(value=np.nan, inplace=True)
                dataframe = OneHotListEncoder().encode(_datapoints, _attribute)
                _data_manager.datapoints.observations = pd.concat([_data_manager.datapoints.observations, dataframe],
                                                                  axis=1)

            return Command(one_hot_encoding_list, '__call__', *args[1:])

    mega_cmd_factory('one_hot_encoding_list')

    return data_manager
