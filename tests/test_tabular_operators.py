import pytest
import inspect


@pytest.fixture
def tabular_operators():
    from so_magic.data.backend.panda_handling.df_backend import PDTabularRetriever, PDTabularIterator, PDTabularMutator
    return {
        'retriever': PDTabularRetriever,
        'iterator': PDTabularIterator,
        'mutator': PDTabularMutator,
    }


@pytest.fixture
def tabular_interfaces():
    from so_magic.data.backend.engine_specs import EngineTabularRetriever, EngineTabularIterator, EngineTabularMutator
    return {
        'retriever': EngineTabularRetriever,
        'iterator': EngineTabularIterator,
        'mutator': EngineTabularMutator,
    }

@pytest.fixture
def tabular_interfaces_contracts():
    return {
        'retriever': {
            'column': '(identifier, data)',
            'row': '(identifier, data)',
            'nb_columns': '(data)',
            'nb_rows': '(data)',
            'get_numerical_attributes': '(data)',
        },
        'iterator': {
            'columnnames': '(data)',
            'itercolumns': '(data)',
            'iterrows': '(data)',
        },
        'mutator': {
            'add_column': '(datapoints, values, new_attribute, **kwargs)',
        },
    }

def test_tabular_interfaces(tabular_interfaces, tabular_operators, tabular_interfaces_contracts):
    
    # RETRIEVER

    pd_tabular_retriever1 = tabular_operators['retriever']()
    pd_tabular_retriever2 = tabular_operators['retriever']()

    expected_implemented_methods_names = list(x[0] for x in inspect.getmembers(
                tabular_interfaces['retriever'], predicate=lambda x: any([inspect.ismethod(x), inspect.isfunction(x)])))

    member1 = list(x[0] for x in inspect.getmembers(pd_tabular_retriever1, predicate=lambda x: any([inspect.ismethod(x), inspect.isfunction(x)])))
    member2 = list(x[0] for x in inspect.getmembers(pd_tabular_retriever2, predicate=lambda x: any([inspect.ismethod(x), inspect.isfunction(x)])))

    for retr_expec_member in expected_implemented_methods_names:
        assert retr_expec_member in member1
        assert retr_expec_member in member1
        sig = inspect.signature(getattr(pd_tabular_retriever1, retr_expec_member))
        assert str(sig) == tabular_interfaces_contracts['retriever']


    assert id(pd_tabular_retriever1._delegate) != id(pd_tabular_retriever2._delegate) 

    for function in tabular_interfaces_contracts['retriever']:
        assert function in dir(pd_tabular_retriever1)
        assert id(getattr(pd_tabular_retriever1, function)) != id(getattr(pd_tabular_retriever2, function))
        assert id(getattr(pd_tabular_retriever1._delegate, function)) != id(getattr(pd_tabular_retriever2._delegate, function))
    


    # ITERATOR

    pd_tabular_iterator1 = tabular_operators['iterator']()
    pd_tabular_iterator2 = tabular_operators['iterator']()

    expected_implemented_methods_names = list(x[0] for x in inspect.getmembers(
                tabular_interfaces['iterator'], predicate=lambda x: any([inspect.ismethod(x), inspect.isfunction(x)])))


    member1 = list(x[0] for x in inspect.getmembers(pd_tabular_iterator1, predicate=lambda x: any([inspect.ismethod(x), inspect.isfunction(x)])))
    member2 = list(x[0] for x in inspect.getmembers(pd_tabular_iterator2, predicate=lambda x: any([inspect.ismethod(x), inspect.isfunction(x)])))

    for retr_expec_member in expected_implemented_methods_names:
        assert retr_expec_member in member1
        assert retr_expec_member in member1
        sig = inspect.signature(getattr(pd_tabular_retriever1, retr_expec_member))
        assert str(sig) == tabular_interfaces_contracts['iterator']


    assert id(pd_tabular_iterator1._delegate) != id(pd_tabular_iterator2._delegate) 

    for function in tabular_interfaces_contracts['iterator']:
        assert function in dir(pd_tabular_iterator1)
        assert id(getattr(pd_tabular_iterator1, function)) != id(getattr(pd_tabular_iterator2, function))
        assert id(getattr(pd_tabular_iterator1._delegate, function)) != id(getattr(pd_tabular_iterator2._delegate, function))


    # MUTATOR

    pd_tabular_mutator1 = tabular_operators['mutator']()
    pd_tabular_mutator2 = tabular_operators['mutator']()

    expected_implemented_methods_names = list(x[0] for x in inspect.getmembers(
                tabular_interfaces['mutator'], predicate=lambda x: any([inspect.ismethod(x), inspect.isfunction(x)])))

    member1 = list(x[0] for x in inspect.getmembers(pd_tabular_mutator1, predicate=lambda x: any([inspect.ismethod(x), inspect.isfunction(x)])))
    member2 = list(x[0] for x in inspect.getmembers(pd_tabular_mutator2, predicate=lambda x: any([inspect.ismethod(x), inspect.isfunction(x)])))

    for retr_expec_member in expected_implemented_methods_names:
        assert retr_expec_member in member1
        assert retr_expec_member in member1
        sig = inspect.signature(getattr(pd_tabular_retriever1, retr_expec_member))
        assert str(sig) == tabular_interfaces_contracts['mutator']

    
    assert id(pd_tabular_mutator1._delegate) != id(pd_tabular_mutator2._delegate) 

    for function in tabular_interfaces_contracts['mutator']:
        assert function in dir(pd_tabular_mutator1)
        assert id(getattr(pd_tabular_mutator1, function)) != id(getattr(pd_tabular_mutator2, function))
        assert id(getattr(pd_tabular_mutator1._delegate, function)) != id(getattr(pd_tabular_mutator2._delegate, function))
