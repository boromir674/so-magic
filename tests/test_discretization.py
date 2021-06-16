import pytest


@pytest.fixture
def define_command():
    def _define_engine_command(decorator, command_function):
        decorator(command_function)
    return _define_engine_command


@pytest.fixture
def get_command(somagic):
    def _get_command(command_name: str):
        return getattr(somagic.command, command_name)
    return _get_command


@pytest.fixture
def test_discretizer():
    from so_magic.data.discretization import Discretizer, BinningAlgorithm

    alg = BinningAlgorithm.from_built_in('pd.cut')

    discretizer = Discretizer.from_algorithm(alg)
    return discretizer


@pytest.fixture
def discretize_command():
    def get_discretize_command(discretizer):
        def test_discretize_command(data_manager, datapoints, attribute, nb_bins, new_column_name):
            output = discretizer.discretize(datapoints, attribute, nb_bins)
            data_manager.datapoints.add_column(output['result'], new_column_name)
        return test_discretize_command
    return get_discretize_command


@pytest.fixture
def validate_discretization_operation_behaviour():
    def _validate_discretization_operation(cmd, algorithm):
        datapoints = cmd.args[0]
        target_column = cmd.args[1]
        nb_bins = cmd.args[2]
        computed_bins = algorithm.output['settings']['used_bins']
        assert [_ for _ in computed_bins] == [-0.1, 25.0, 50.0, 75.0, 100.0]

        input_arguments = algorithm.output['settings']['arguments']
        to_check = [len(input_arguments[0]), input_arguments[1]]
        assert to_check == [len(datapoints), nb_bins]
        assert type(datapoints.column(target_column)) == type(input_arguments[0])
        assert list(datapoints.column(target_column)) == list(input_arguments[0])
        # assert algorithm.output['settings']['parameters'] == []
    return _validate_discretization_operation


@pytest.fixture
def discretization_test_data(somagic, test_datapoints):
    series = somagic.dataset.datapoints.column('Creative').replace('', 0.0, inplace=False)
    assert all(type(x) == float for x in series)

    somagic.datapoints.add_column(list(series), 'Creative')

    
    assert all(type(x) == float for x in somagic.datapoints.observations['Creative'])

    return {
        'success': [
            'Creative'
        ],
        'fail': [
            'Energetic'
        ],
    }


def test_discretization_operation(somagic, discretization_test_data, define_command, get_command, test_discretizer, discretize_command, validate_discretization_operation_behaviour):
    define_command(somagic.commands_decorators.data_manager_command(), discretize_command(test_discretizer))
    for attr_name in discretization_test_data['success']:
        cmd = get_command('test_discretize_command')
        cmd.args = [somagic.datapoints, attr_name, 4, f'binned_{attr_name}']
        cmd.execute()

        validate_discretization_operation_behaviour(cmd, test_discretizer.algorithm)

    for attr_name in discretization_test_data['fail']:
        cmd = get_command('test_discretize_command')
        cmd.args = [somagic.datapoints, attr_name, 4, f'binned_{attr_name}']
        with pytest.raises(TypeError):
            cmd.execute()
