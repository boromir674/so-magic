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


    return data_manager
