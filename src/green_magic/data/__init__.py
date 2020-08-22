from .data_manager import DataManager
from .backend import magic_backend
from .features.phi import PhiFunction

data_manager = DataManager(magic_backend)
PhiFunction.subject.attach(data_manager.built_phis)


from green_magic.data.command_factories import NominalAttributeListEncodeCommandFactory
fct = NominalAttributeListEncodeCommandFactory

@data_manager.backend.engine.dec()
def encode_nominal_subsets(datapoints, attribute, new_attribute):
    from green_magic.data.features.phis import ListOfCategoricalPhi, DatapointsAttributePhi
    phi = ListOfCategoricalPhi(DatapointsAttributePhi(datapoints))
    new_values = phi(attribute)
    datapoints.mutator.add_column(datapoints, new_values, new_attribute)
