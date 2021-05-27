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


def test_tabular_interfaces(tabular_interfaces, tabular_operators):
    expected_contract = {
        'retriever': ['column', 'row', 'nb_columns', 'nb_rows', 'get_numerical_attributes'],
        'iterator': ['columnnames', 'itercolumns', 'iterrows'],
    }

    retr_members = ['column', 'row', 'nb_columns', 'nb_rows', 'get_numerical_attributes']

    

    pd_tabular_retriever1 = tabular_operators['retriever']()
    pd_tabular_retriever2 = tabular_operators['retriever']()

    member1 = list(x[0] for x in inspect.getmembers(pd_tabular_retriever1))
    member2 = list(x[0] for x in inspect.getmembers(pd_tabular_retriever2))

    for exp_member in retr_members:
        assert exp_member in member1
        assert exp_member in member2

    class A:
        def go(self, x):
            return x + 1
        @staticmethod
        def ela(y):
            return y - 1
        @classmethod
        def pame(cls, z):
            return z * 2
    
    a = A()

    go_sig = inspect.signature(a.go)
    ela_sig = inspect.signature(a.ela)
    pame_sig = inspect.signature(a.pame)

    assert str(go_sig) == '(x)'
    assert str(ela_sig) == '(y)'
    assert str(pame_sig) == '(z)'
    
    for method in retr_members[:2]:
        sig = inspect.signature(getattr(pd_tabular_retriever1, method))
        assert str(sig) == '(identifier, data)'

    for method in retr_members[2:]:
        sig = inspect.signature(getattr(pd_tabular_retriever1, method))
        assert str(sig) == '(data)'

    assert id(pd_tabular_retriever1._delegate) != id(pd_tabular_retriever2._delegate) 

    for function in expected_contract['retriever']:
        assert function in dir(pd_tabular_retriever1)
        assert id(getattr(pd_tabular_retriever1, function)) != id(getattr(pd_tabular_retriever2, function))
        assert id(getattr(pd_tabular_retriever1._delegate, function)) != id(getattr(pd_tabular_retriever2._delegate, function))

    # pd_tabular_iterator1 = tabular_operators['iterator']()
    # pd_tabular_iterator2 = tabular_operators['iterator']()
    # assert id(pd_tabular_iterator1._delegate) != id(pd_tabular_iterator2._delegate)
    # for f in expected_contract['iterator']:
    #     assert f in dir(pd_tabular_iterator1)
    #     assert f in dir(pd_tabular_iterator2)
    #     assert id(getattr(pd_tabular_iterator1, f)) != id(getattr(pd_tabular_iterator2, f))
    #     assert id(getattr(pd_tabular_iterator1._delegate, f)) != id(getattr(pd_tabular_iterator2._delegate, f))