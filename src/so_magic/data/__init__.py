from .data_manager import DataManager
from .features.phi import PhiFunctionRegistrator
from .features import FeatureManager
from .command_factories import DataManagerCommandFactory

from .built_in_commands import encode_nominal_subsets_command
from .built_in_data_manager_commands import select_variables_command
from .pd_commands import data_manager_commands, arbitrary_commands


def init_data_manager(engine):
    # Initialize DataManager instance and DataManagerCommandFactory
    my_data_manager = DataManager(
        engine,
        type('PhiFunction', (PhiFunctionRegistrator,), {}),
        FeatureManager([]),
    )
    mega_cmd_factory = DataManagerCommandFactory(my_data_manager)
    mega_cmd_factory.subject.attach(my_data_manager.commands_manager.command.accumulator)

    my_data_manager.commands_manager.decorators = type('EngineCommandDecorators', (object,), {
        'data_manager_command': mega_cmd_factory.build_command_prototype,
        'arbitrary_command': my_data_manager.engine.backend.dec,
    })()

    # Build backend-agnostic, built-in engine commands
    my_data_manager.engine.backend.dec()(encode_nominal_subsets_command)
    mega_cmd_factory.build_command_prototype()(select_variables_command)

    # Build backend-dependent (eg dependent on pandas) client engine commands
    for arbitrary_cmd in arbitrary_commands:
        my_data_manager.engine.backend.dec()(arbitrary_cmd)

    for data_manager_cmd in data_manager_commands:
        mega_cmd_factory.build_command_prototype()(data_manager_cmd)

    return my_data_manager
