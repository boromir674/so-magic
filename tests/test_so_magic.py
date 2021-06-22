import pytest


@pytest.fixture
def assert_selected_variables_are(somagic):
    def _assert_selected_variables_are(variables: set):
        assert set([x['variable'] for x in somagic._data_manager.feature_manager.feature_configuration.variables]) == variables
    return _assert_selected_variables_are


@pytest.fixture
def assert_column_values(test_dataset):
    import pandas as pd

    def _assert_column_values_are(attribute, expected_values):
        assert set([_ for _ in test_dataset[0].datapoints.observations[attribute]]) == set(expected_values)
        assert set(pd.unique(test_dataset[0].datapoints.observations[attribute])) == set(expected_values)
    return _assert_column_values_are


@pytest.fixture
def assert_correct_nominal_variable_encoding(test_dataset):
    """Test a column with each row having a string representing one of the possible values of an Attrbiute.

    Useful when an Attribute corresponds to a discreet Variable of type Nominal (ordering does not matter) and its
    observation (row) can have only one of the possible values.
    """
    from collections import Counter

    def _assert_nominal_variable_encoded_as_expected(expected_feature_columns):
        assert all(Counter([datarow[_] for _ in expected_feature_columns]) ==
                   Counter({0: len(expected_feature_columns) - 1, 1: 1})
                   for index, datarow in test_dataset[0].datapoints.observations[expected_feature_columns].iterrows())
    return _assert_nominal_variable_encoded_as_expected


def test_sanity_checks_on_dataset(test_dataset, assert_selected_variables_are, assert_column_values,
                                  assert_correct_nominal_variable_encoding):
    ATTRS2 = [f'type_{x}' for x in test_dataset[1]]

    datapoints = test_dataset[0].datapoints
    assert_selected_variables_are({'type', 'flavors'})

    assert all(type(x) == str for x in datapoints.observations['type'])

    assert_column_values('type', expected_values=test_dataset[1])

    assert_correct_nominal_variable_encoding(ATTRS2)

    # the below is expected because test_dataset invokes the 'one_hot_encoding_list_command' command which unfortunately
    # at the moment has a side effect on the attribute it operates on.
    # side effect: _data_manager.datapoints.observations[_attribute].fillna(value=np.nan, inplace=True)
    assert set([type(x) for x in datapoints.observations['flavors']]) == {list, float}

    assert len(test_dataset[2]) > 5

    assert all(x in datapoints.observations.columns for x in test_dataset[2])
    assert all(0 <= sum([datarow[_] for _ in test_dataset[2]]) <= test_dataset[3]
               for index, datarow in datapoints.observations[list(test_dataset[2])].iterrows())

    assert hasattr(test_dataset[0], 'feature_vectors')


@pytest.mark.parametrize('train_args', [
    ([6, 8, 'toroid', 'hexagonal']),
    # ([12, 12, 'toroid', 'rectangular'])
])
def test_somagic_scenario(train_args, somagic, test_dataset, sample_collaped_json):
    attrs = ('width', 'height', 'type', 'grid_type')
    som = somagic.map.train(*train_args[:2], maptype=train_args[2], gridtype=train_args[3])
    assert som.dataset_name == sample_collaped_json
    assert all(parameter == getattr(som, attribute) for attribute, parameter in zip(attrs, train_args))


@pytest.fixture
def so_magic_instances():
    from so_magic import init_so_magic
    return [init_so_magic(), init_so_magic()]


@pytest.mark.parametrize('nb_objects, nb_observers', [
    (2, [(1, 1, 1),
         (1, 1, 1)]),
])
def test_somagic_objects(nb_objects, so_magic_instances, nb_observers):
    assert id(so_magic_instances[0]) != id(so_magic_instances[1])
    assert id(so_magic_instances[0]._data_manager) != id(so_magic_instances[1]._data_manager)
    assert id(so_magic_instances[0]._data_manager.engine) != id(so_magic_instances[1]._data_manager.engine)
    assert id(so_magic_instances[0]._data_manager.engine.backend) != id(so_magic_instances[1]._data_manager.engine.backend)
    assert id(so_magic_instances[0]._data_manager.engine.datapoints_manager) != id(so_magic_instances[1]._data_manager.engine.datapoints_manager)

    assert id(so_magic_instances[0]._data_manager.engine.backend.datapoints_factory) != id(so_magic_instances[1]._data_manager.engine.backend.datapoints_factory)
    assert id(so_magic_instances[0]._data_manager.engine.backend.datapoints_factory.subject) != id(so_magic_instances[1]._data_manager.engine.backend.datapoints_factory.subject)
    assert id(so_magic_instances[0]._data_manager.engine.backend.datapoints_factory.subject._observers) != id(so_magic_instances[1]._data_manager.engine.backend.datapoints_factory.subject._observers)

    assert id(so_magic_instances[0]._data_manager.engine.backend.command_factory) != id(so_magic_instances[1]._data_manager.engine.backend.command_factory)

    assert so_magic_instances[0]._data_manager.phi_class != so_magic_instances[1]._data_manager.phi_class
    assert id(so_magic_instances[0]._data_manager.phi_class) != id(so_magic_instances[1]._data_manager.phi_class)
    assert id(so_magic_instances[0]._data_manager.phi_class.subject) != id(so_magic_instances[1]._data_manager.phi_class.subject)
    assert id(so_magic_instances[0]._data_manager.phi_class.subject._observers) != id(so_magic_instances[1]._data_manager.phi_class.subject._observers)


def test_subscriptions(so_magic_instances):
    s = so_magic_instances[0]
    datapoints_fact = s._data_manager.engine.backend.datapoints_factory
    cmd_fact = s._data_manager.engine.backend.command_factory
    phi_class = s._data_manager.phi_class
    nb_observers = (1, 1, 1)
    subjects = [datapoints_fact.subject,
                cmd_fact.subject,
                phi_class.subject
                ]

    assert datapoints_fact.subject._observers[0] == s._data_manager.engine.datapoints_manager
    assert cmd_fact.subject._observers[0] == s._data_manager.commands_manager.command.accumulator
    assert phi_class.subject._observers[0] == s._data_manager.built_phis
    assert all([len(subject._observers) == column for subject, column in zip(subjects, nb_observers)])
