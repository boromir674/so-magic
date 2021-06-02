import pytest


@pytest.fixture
def data_manager_command_decorator(test_data_manager):
    return test_data_manager.commands_manager.decorators.data_manager_command


@pytest.fixture
def define_command(data_manager_command_decorator):
    def _define_engine_command(data_manager):
        pass
        # from so_magic.data.discretization import 
        # @data_manager_command_decorator()
        # def discretize_to_intervals_command(_data_manager, datapoints, new_column):
    return _define_engine_command


def test_discretization_operation(test_data_manager, load_test_data, define_command):
    load_test_data()
    define_command(test_data_manager)
    # discretization_cmd = get_command('discretization')
    # discretization_cmd.args = [test_data]
    # discretization_cmd.run()

    # validate_discretization_operation_behaviour()
