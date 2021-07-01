import pytest
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
    assert all([type(x) == list for x in dt_manager.datapoints.column('flavors')])

    cmd = dt_manager.command.encode_nominal_subsets_command
    cmd.args = [dt_manager.datapoints, 'flavors', 'encoded_flavors']
    cmd.execute()

    # assert set(dt_manager.datapoints.attributes) == set(_ for _ in list(test_json_data['attributes']) + ['encoded_flavors'])
