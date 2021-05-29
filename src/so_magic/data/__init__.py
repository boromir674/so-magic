from .data_manager import DataManager
from .features.phi import PhiFunctionRegistrator
from .features import FeatureManager
from .command_factories import DataManagerCommandFactory

from .built_in_commands import encode_nominal_subsets_command
from .built_in_data_manager_commands import select_variables_command
from .pd_commands import data_manager_commands, arbitrary_commands


def init_data_manager(a_backend):
    # Initialize DataManager instance and DataManagerCommandFactory
    my_data_manager = DataManager(a_backend, type('PhiFunction', (PhiFunctionRegistrator,), {}), FeatureManager([]))
    mega_cmd_factory = DataManagerCommandFactory(my_data_manager)
    mega_cmd_factory.attach(my_data_manager.commands_manager.command.accumulator)

    # Build backend-agnostic, built-in engine commands
    my_data_manager.backend.engine.dec()(encode_nominal_subsets_command)
    mega_cmd_factory.build_command_prototype()(select_variables_command)

    # Build backend-dependent (eg dependent on pandas) client engine commands
    for arbitrary_cmd in arbitrary_commands:
        my_data_manager.backend.engine.dec()(arbitrary_cmd)

    for data_manager_cmd in data_manager_commands:
        mega_cmd_factory.build_command_prototype()(data_manager_cmd)

    return my_data_manager
