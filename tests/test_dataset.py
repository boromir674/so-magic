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
