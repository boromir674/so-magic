from functools import reduce
from .data_manager import DataManager
from .features.phi import PhiFunctionRegistrator
from .features import FeatureManager
from .command_factories import DataManagerCommandFactory


def init_data_manager(a_backend):
    data_manager = DataManager(a_backend, type('PhiFunction', (PhiFunctionRegistrator,), {}), FeatureManager([]))
    mega_cmd_factory = DataManagerCommandFactory(data_manager)
    mega_cmd_factory.attach(data_manager.commands_manager.command.accumulator)

    # Build built-in engine commands
    from .built_in_commands import encode_nominal_subsets_command
    data_manager.backend.engine.dec()(encode_nominal_subsets_command)
    
    from .built_in_data_manager_commands import select_variables_command
    mega_cmd_factory.build_command_prototype()(select_variables_command)

    import pandas as pd

    @data_manager.backend.engine.dec()
    def observations_command(file_path):
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
    def one_hot_encoding_command(_data_manager, _datapoints, _attribute):
        dataframe = OneHotEncoder().encode(_datapoints, _attribute)
        # TODO add a add_columns method to the mutator interface
        # replace below with datapoints.mutator.add_columns(...) (similar to the encode_nominal_subsets_command above)
        _data_manager.datapoints.observations = pd.concat([_data_manager.datapoints.observations, dataframe], axis=1)

    import numpy as np

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

    @mega_cmd_factory.build_command_prototype()
    def one_hot_encoding_list_command(_data_manager, _datapoints, _attribute):
        _data_manager.datapoints.observations[_attribute].fillna(value=np.nan, inplace=True)
        dataframe = OneHotListEncoder().encode(_datapoints, _attribute)
        _data_manager.datapoints.observations = pd.concat([_data_manager.datapoints.observations, dataframe],
                                                            axis=1)

    return data_manager
