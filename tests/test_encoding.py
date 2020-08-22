import pytest

def test_encoding_list_nominal(data_manager, datapoints, test_json_data):
    cmd = data_manager.command.encode_nominal_subsets
    cmd.args = [data_manager.datapoints, 'flavors', 'encoded_flavors']

    cmd.execute()

    assert set(data_manager.datapoints.attributes) == set(_ for _ in list(test_json_data['attributes']) + ['encoded_flavors'])
    assert set(datapoints.attributes) == set(_ for _ in list(test_json_data['attributes']) + ['encoded_flavors'])

