import pytest


@pytest.fixture
def client_pandas_tabular_implementation():
    from so_magic.data.interfaces import TabularRetriever, TabularIterator, TabularMutator
    
    class TestPDTabularRetrieverDelegate(TabularRetriever):
        """The observation object is the same as the one you return from 'from_json_lines'"""

        @classmethod
        def column(cls, identifier, data):
            return data.observations[identifier]

        def row(self, identifier, data):
            return data.observations.loc(identifier)

        @classmethod
        def nb_columns(cls, data):
            return len(data.observations.columns)

        @classmethod
        def nb_rows(cls, data):
            return len(data.observations)

        @classmethod
        def get_numerical_attributes(cls, data):
            return data.observations._get_numeric_data().columns.values


    class TestPDTabularIteratorDelegate(TabularIterator):
        """The observation object is the same as the one your return from 'from_json_lines'"""

        def columnnames(self, data):
            return list(data.observations.columns)

        @classmethod
        def iterrows(cls, data):
            return iter(data.observations.iterrows())

        @classmethod
        def itercolumns(cls, data):
            return iter(data.observations[column] for column in data.observations.columns)


    class TestPDTabularMutatorDelegate(TabularMutator):

        @classmethod
        def add_column(cls, datapoints, values, new_attribute, **kwargs):
            datapoints.observations[new_attribute] = values


    BACKEND = {
        'backend_id': 'test-pd',
        'backend_name': 'test-pandas',
        'interfaces': [
            TestPDTabularRetrieverDelegate,
            TestPDTabularIteratorDelegate,
            TestPDTabularMutatorDelegate,
        ]
    }

    return BACKEND


@pytest.fixture
def engine_backends(client_pandas_tabular_implementation):
    CLIENT_BACKENDS = [
        client_pandas_tabular_implementation,
    ]
    from so_magic.data.backend.panda_handling.df_backend import magic_backends

    backends = magic_backends()

    backends.add(*CLIENT_BACKENDS)
    return backends


def test_delegate_sanity_check(engine_backends, data_manager):
    dt_manager = data_manager()
    # assert that the data engine initial (default) backend is "pandas-backend"
    # could need to change in the future if we give the client the option to initialize the engine with a backend of their preference
    assert dt_manager.engine.backend.id == 'pd'
    for backend_id, _backend_implementation in engine_backends:
        dt_manager.engine.backend = engine_backends.backends[backend_id]
        assert dt_manager.engine.backend.id == backend_id
