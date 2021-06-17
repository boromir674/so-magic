import inspect
import pytest


@pytest.fixture
def client_pandas_tabular_implementation():
    """Client code that defines an Engine Backend"""
    from so_magic.data.interfaces import TabularRetriever, TabularIterator, TabularMutator
    
    class TestPDTabularRetrieverDelegate(TabularRetriever):

        @classmethod
        def column(cls, identifier, data):
            return inspect.currentframe().f_code.co_name

        def row(self, identifier, data):
            return inspect.currentframe().f_code.co_name

        @classmethod
        def nb_columns(cls, data):
            return inspect.currentframe().f_code.co_name

        @classmethod
        def nb_rows(cls, data):
            return inspect.currentframe().f_code.co_name

        @classmethod
        def get_numerical_attributes(cls, data):
            return inspect.currentframe().f_code.co_name

    class TestPDTabularIteratorDelegate(TabularIterator):

        def columnnames(self, data):
            return inspect.currentframe().f_code.co_name

        @classmethod
        def iterrows(cls, data):
            return inspect.currentframe().f_code.co_name

        @classmethod
        def itercolumns(cls, data):
            return inspect.currentframe().f_code.co_name

    class TestPDTabularMutatorDelegate(TabularMutator):

        @classmethod
        def add_column(cls, datapoints, values, new_attribute, **kwargs):
            return inspect.currentframe().f_code.co_name

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
def built_in_n_client_backends(built_in_backends, client_pandas_tabular_implementation):
    CLIENT_BACKENDS = [
        client_pandas_tabular_implementation,
    ]

    built_in_backends.add(*CLIENT_BACKENDS)
    return built_in_backends


def test_delegate_sanity_check(built_in_n_client_backends, tabular_operators, data_manager):
    dt_manager = data_manager()
    # assert that the data engine initial (default) backend is "pandas-backend"
    # could need to change in the future if we give the client the option to initialize the engine with a backend of
    # their preference
    assert dt_manager.engine.backend.id == 'pd'

    for backend_id, implementations_data in built_in_n_client_backends:
        dt_manager.engine.backend = built_in_n_client_backends.backends[backend_id]
        assert dt_manager.engine.backend.id == backend_id
        assert all(all(required_method_name in dir(implementations_data[operator_interface_name])
                       for required_method_name in required_methods)
                   for operator_interface_name, required_methods in tabular_operators['required_methods'])

    for operator_interface_name, required_methods in tabular_operators['required_methods']:
        for m in required_methods:
            nb_args = tabular_operators['get_nb_args'](operator_interface_name, m)
            # we have to initialize an instance out of an operator class like we do in the 'observations_command' method in the Backend
            # class (eg cls.retriever(), cls.iterator(), cls.mutator())
            assert getattr(built_in_n_client_backends.implementations['test-pd'][operator_interface_name](), m)(*list([None] * nb_args)) == m

        # assert all(getattr(built_in_n_client_backends.implementations['test-pd'][operator_interface_name], method)(None, None) == method for method in required_methods)
