import pytest
from functools import reduce
import math
from collections import Counter
import numpy as np
from pandas import isnull


@pytest.fixture
def eliminate_nan_n_None_command(somagic, test_datapoints):

    def _eliminate_nan_n_None_command(_data_manager, datapoints, attribute):
        c = Counter([type(x) for x in datapoints.column(attribute)])
        majority_type, max_value = c.most_common()[0]
        assert majority_type == list

        def check(x, target_type):
            try:
                if isnull(x):  # True for both np.nan and None
                    return target_type()
            except ValueError:
                pass
            return x
        datapoints.observations[attribute] = datapoints.observations[attribute].map(lambda a: check(a, majority_type))
        assert all([type(x) == majority_type for x in datapoints.column(attribute)])

    somagic.commands_decorators.data_manager_command()(_eliminate_nan_n_None_command)
    return getattr(somagic.command, _eliminate_nan_n_None_command.__name__)


def test_encoding_list_nominal(somagic, test_datapoints,
                               eliminate_nan_n_None_command,
                               datapoint_files_to_test,
                               assert_correct_one_hot_encoding,
                               assert_correct_one_hot_encodingof_list
                               ):
    dt_manager = somagic._data_manager
    assert len(dt_manager.engine.datapoints_manager.datapoints_registry.objects) == 1

    from collections import Counter
    c = Counter([type(x) for x in dt_manager.datapoints.column('flavors')])
    assert c == Counter({list: 98, type(None): 2})

    cmd = eliminate_nan_n_None_command
    cmd.args = [somagic.datapoints, 'flavors']
    cmd.execute()

    c = Counter([type(x) for x in dt_manager.datapoints.column('flavors')])
    assert c == Counter({list: 100})
    
    assert list(datapoint_files_to_test['data_1']['column_names']) == dt_manager.datapoints.attributes

    cmd = dt_manager.command.encode_command
    cmd.args = [type('Variable', (object,), {
        'type': 'nominal',
        'data_type': str,
        '__str__': lambda self: 'type',
    })()]
    cmd.execute()

    nb_added_columns = len(dt_manager.datapoints.attributes) - len(datapoint_files_to_test['data_1']['column_names'])
    runtime_feature_names = list(dt_manager.datapoints.attributes)[-nb_added_columns:]

    expected_feature_columns = [f'type_{x}' for x in ('hybrid', 'indica', 'sativa')]
    assert_correct_one_hot_encoding(somagic._data_manager.datapoints, expected_feature_columns)

    assert list(datapoint_files_to_test['data_1']['column_names']) + runtime_feature_names == dt_manager.datapoints.attributes

    cmd = dt_manager.command.encode_command
    cmd.args = [type('Variable', (object,), {
        'type': 'nominal',
        'data_type': list,
        '__str__': lambda self: 'flavors',
    })()]
    cmd.execute()

    UNIQUE_FLAVORS = reduce(lambda i, j: set(i).union(set(j)),
                            [_ for _ in somagic._data_manager.datapoints.observations['flavors'] if _ is not None])

    assert_correct_one_hot_encodingof_list(somagic._data_manager.datapoints, ['flavors_' + x for x in UNIQUE_FLAVORS])

    nb_added_columns = len(dt_manager.datapoints.attributes) - len(datapoint_files_to_test['data_1']['column_names']) - nb_added_columns
    runtime_flavors_feature_names = list(dt_manager.datapoints.attributes)[-nb_added_columns:]

    assert list(datapoint_files_to_test['data_1']['column_names']) + runtime_feature_names + runtime_flavors_feature_names == dt_manager.datapoints.attributes


@pytest.fixture
def assert_correct_one_hot_encoding():
    from collections import Counter
    from typing import List
    def _assert_correct_one_hot_encoding(datapoints, feature_columns: List[str]):
        assert all([Counter([datarow[_] for _ in feature_columns]) == Counter({0: len(feature_columns) - 1, 1: 1}) for index, datarow in datapoints.observations[feature_columns].iterrows()])
    return _assert_correct_one_hot_encoding


@pytest.fixture
def assert_correct_one_hot_encodingof_list():
    from collections import Counter
    from typing import List
    def _assert_correct_one_hot_encoding(datapoints, feature_columns: List[str]):
        assert all([0 <= sum([datarow[_] for _ in feature_columns]) <= len(feature_columns) for index, datarow in datapoints.observations[feature_columns].iterrows()])
    return _assert_correct_one_hot_encoding
