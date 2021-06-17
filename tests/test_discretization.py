import pytest


@pytest.fixture
def define_command():
    def _define_engine_command(decorator, command_function):
        decorator(command_function)
        return command_function.__name__
    return _define_engine_command


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
def discretization_cmd(somagic, test_datapoints, define_command, discretize_command, test_discretizer):
    """Get a discretization command after some 'pre-processing' done on the test datapoints."""
    series = somagic.dataset.datapoints.column('Creative').replace('', 0.0, inplace=False)
    assert all(type(x) == float for x in series)

    somagic.datapoints.add_column(list(series), 'Creative')

    assert all(type(x) == float for x in somagic.datapoints.observations['Creative'])

    test_discretize_command_name: str = define_command(somagic.commands_decorators.data_manager_command(),
                                                       discretize_command(test_discretizer))
    return getattr(somagic.command, test_discretize_command_name)


@pytest.fixture(params=[
    ['Creative'],
    # [],  # add more columns when we know the discretization command will succeed for them
])
def cmd_to_succeed(request, test_datapoints, discretization_cmd):
    discretization_cmd.args = [test_datapoints, request.param[0], 4, f'binned_{request.param[0]}']
    return discretization_cmd


def test_discretization_operation(cmd_to_succeed, test_discretizer, validate_discretization_operation_behaviour):
    cmd_to_succeed.execute()
    validate_discretization_operation_behaviour(cmd_to_succeed, test_discretizer.algorithm)


@pytest.fixture(params=[
    ['Energetic'],
    # [],  # add more columns when we know the discretization command will fail for them
])
def cmd_to_fail(request, test_datapoints, discretization_cmd):
    discretization_cmd.args = [test_datapoints, request.param[0], 4, f'binned_{request.param[0]}']
    return discretization_cmd


def test_discretization_on_non_preprocessed_attribute(cmd_to_fail):
    with pytest.raises(TypeError):
        cmd_to_fail.execute()
