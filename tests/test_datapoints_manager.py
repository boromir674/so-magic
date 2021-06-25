import pytest


@pytest.fixture
def datapoints_manager_infra():
    from so_magic.data.datapoints_manager import DatapointsManager, NonExistantDatapointsError
    return type('DatapointsManagerInfra', (object,), {
        'DatapointsManager': DatapointsManager(),
        'exceptions': type('E', (object,), {
            'store_with_invalid_key': Exception,
            'store_with_existing_key': Exception,
            'retrieve_non_existing_key': NonExistantDatapointsError,
        }),
    })


@pytest.fixture
def test_subjects():
    return type('S', (object,), {'empty_key': type('DynamicSubject', (object,), {'state': [1], 'name': ''}),
                                 'k1': type('DynamicSubject', (object,), {'state': [1], 'name': 'k1'})})


def test_registering_datapoints_with_invalid_key(datapoints_manager_infra, test_subjects):
    with pytest.raises(datapoints_manager_infra.exceptions.store_with_invalid_key,
                       match=rf'Subject {test_subjects.empty_key} with state \[1\] resulted in an empty string as key. '
                             r'We reject the key, since it is going to "query" a dict/hash\.'):
        datapoints_manager_infra.DatapointsManager.update(test_subjects.empty_key)

def test_registering_datapoints_with_existing_key(datapoints_manager_infra, test_subjects):
    datapoints_manager_infra.DatapointsManager.update(test_subjects.k1)
    with pytest.raises(datapoints_manager_infra.exceptions.store_with_existing_key):
        datapoints_manager_infra.DatapointsManager.update(test_subjects.k1)


def test_retrieving_non_registered_datapoints(caplog, datapoints_manager_infra):
    with pytest.raises(datapoints_manager_infra.exceptions.retrieve_non_existing_key,
                       match=r'Requested non existant Datapoints instance. Probable cause is that this \(self\) '
                             'DatapointsManager instance has not been notified by a DatapointsFactory'):
        _ = datapoints_manager_infra.DatapointsManager.datapoints
    assert 'Non existant Datapoints: {\n' \
           '  "last-key-used-to-register-datapoints": "",\n' \
           '  "datapoints-registry-keys": "[]"\n}' in caplog.text
