def test_encoding_list_nominal(data_manager, test_json_data):
    dt_manager = data_manager()
    cmd = dt_manager.command.observations_command
    cmd.args = [test_json_data['file_path']]
    assert dt_manager.engine.datapoints_manager.datapoints_objects == {}
    cmd.execute()
    assert len(dt_manager.engine.datapoints_manager.datapoints_objects) == 1

    cmd = dt_manager.command.encode_nominal_subsets_command
    cmd.args = [dt_manager.datapoints, 'flavors', 'encoded_flavors']
    cmd.execute()

    assert set(dt_manager.datapoints.attributes) == set(_ for _ in list(test_json_data['attributes']) + ['encoded_flavors'])
