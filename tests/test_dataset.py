import pytest


@pytest.fixture
def assert_selected_variables_are(somagic):
    def _assert_selected_variables_are(variables: set):
        assert set([x['variable'] for x in somagic._data_manager.feature_manager.feature_configuration.variables]) == variables
    return _assert_selected_variables_are


@pytest.fixture
def assert_column_values(test_dataset):
    """Assert that the set of some tabular data column's values is equal to the given set."""
    import pandas as pd

    def _assert_column_values_are(attribute, expected_values):
        assert set([_ for _ in test_dataset[0].datapoints.observations[attribute]]) == set(expected_values)
        assert set(pd.unique(test_dataset[0].datapoints.observations[attribute])) == set(expected_values)
    return _assert_column_values_are


@pytest.fixture
def assert_correct_nominal_variable_encoding(test_dataset):
    """Test a column with each row having a string representing one of the possible values of an Attribute.

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
    expected_feature_columns = [f'type_{x}' for x in test_dataset[1]]
    flavors_feature_column_names = ['flavors_' + x for x in test_dataset[2]]
    print('expected_feature_columns:', expected_feature_columns)
    datapoints = test_dataset[0].datapoints
    assert_selected_variables_are({'type', 'flavors'})

    assert all(type(x) == str for x in datapoints.observations['type'])

    assert_column_values('type', expected_values=test_dataset[1])

    from collections import Counter
    for index, datarow in test_dataset[0].datapoints.observations[expected_feature_columns].iterrows():
        assert Counter([datarow[_] for _ in expected_feature_columns]) == Counter({0: len(expected_feature_columns) - 1, 1: 1})

    assert set([type(x) for x in datapoints.observations['flavors']]) == {list}

    assert len(test_dataset[2]) > 5

    assert all(x in datapoints.observations.columns for x in flavors_feature_column_names)
    assert all(0 <= sum([datarow[_] for _ in flavors_feature_column_names]) <= test_dataset[3]
               for index, datarow in datapoints.observations[flavors_feature_column_names].iterrows())

    assert hasattr(test_dataset[0], 'feature_vectors')
