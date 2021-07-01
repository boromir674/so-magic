import pytest
from collections import Counter


@pytest.fixture(params=[
    ['data_1'],
    ['data_2'],
])
def test_data(request, somagic, datapoint_files_to_test, read_observations):
    test_datapoints_json_file = datapoint_files_to_test[request.param[0]]['data_path']
    read_observations(somagic, test_datapoints_json_file)
    return type('T', (object,), {
        'dataset': somagic.dataset,
        'expected_data': datapoint_files_to_test[request.param[0]],
        'expected_dataset_name': test_datapoints_json_file,
    })


def test_table_dimensions(test_data):
    assert test_data.dataset.name == test_data.expected_dataset_name
    assert len(test_data.dataset.datapoints) == test_data.dataset.datapoints.nb_rows == test_data.expected_data['nb_rows']
    assert test_data.dataset.datapoints.nb_columns == test_data.expected_data['nb_columns']
    assert tuple(test_data.dataset.datapoints.attributes) == test_data.expected_data['column_names']
    
    assert all([Counter([type(x) for x in test_data.dataset.datapoints.column(k)]) ==
                Counter(v) for k, v in test_data.expected_data['type_distros'].items()])

    assert all([Counter([x for x in test_data.dataset.datapoints.column(k)]) ==
                Counter(v) for k, v in test_data.expected_data['value_distros'].items()])

    # Uncomment below to debug the complex assert statement with triple all, below
    # print()
    # for row, v in test_data.expected_data['row'].items():
    #     print('ROW', row)
    #     for j, (column, value) in enumerate(v.items()):
    #         print(j, 'Column:', column, 'Value:', value)
    #         for k, condition in enumerate(value):
    #             print('Condition index:', k)
    #             assert condition(test_data.dataset.datapoints.row(row)[column])
    

    # for i, v in enumerate(test_data.dataset.datapoints.column('flavors')):
    #     print('I:', i)
    #     if i < 76:
    #         assert type(v) == list
    #     if i == 76:
    #         # assert type(v) == list
    #         assert type(v) == type(None)
    #     if i > 76 and i < 87:
    #         assert type(v) == list
    #     if i == 87:
    #         # assert type(v) == list
    #         assert type(v) == type(None)
    #     if i > 87:
    #         assert type(v) == list

    assert all([all([all([condition(test_data.dataset.datapoints.row(row)[column]) for condition in value])
                     for column, value in v.items()]) for row, v in test_data.expected_data['row'].items()])
