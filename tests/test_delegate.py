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


@pytest.fixture(params=[
    ['test-pd'],  # client backend
    ['pd'],  # so magic built in (default) backend
])
def engine_backend(request, built_in_n_client_backends):
    return built_in_n_client_backends.backends[request.param[0]]


def test_delegate_sanity_check2(built_in_n_client_backends, engine_backend, tabular_operators, data_manager):
    dt_manager = data_manager()
    assert dt_manager.engine.backend.id == 'pd'

    dt_manager.engine.backend = engine_backend
    assert dt_manager.engine.backend.id == engine_backend.id
    assert all(all(hasattr(getattr(engine_backend, operator_interface_name)(), required_method_name)
                   for required_method_name in required_methods)
               for operator_interface_name, required_methods in tabular_operators['required_methods'])


def test_client_backend(built_in_n_client_backends, tabular_operators):
    # just invoke all methods of each operator as a 'smoke test'
    assert all(all(getattr(built_in_n_client_backends.implementations['test-pd'][operator_interface_name](), m)
                   (*list([None] * tabular_operators['get_nb_args'](operator_interface_name, m))) == m
                   for m in required_methods)
               for operator_interface_name, required_methods in tabular_operators['required_methods'])
