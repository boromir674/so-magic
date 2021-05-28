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
def tabular_operators_reverse():
    from so_magic.data.backend.panda_handling.df_backend import PDTabularRetriever, PDTabularIterator, PDTabularMutator
    return {
        PDTabularRetriever: 'retriever',
        PDTabularIterator: 'iterator',
        PDTabularMutator: 'mutator',
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


@pytest.fixture
def member_names():
    def get_member_names(_object):
        return list(x[0] for x in inspect.getmembers(_object, predicate=lambda x: any([inspect.ismethod(x), inspect.isfunction(x)])))    
    return get_member_names


@pytest.fixture
def create_instances(tabular_operators):
    def _create_operators(*interface_ids):
        return tuple(tabular_operators[interface_id]() for interface_id in interface_ids)
    return _create_operators


@pytest.fixture
def assert_correct_signatures(tabular_interfaces_contracts, member_names, tabular_operators_reverse):
    def _assert_correct_signatures(instance):
        interface_id = tabular_operators_reverse[type(instance)]
        expected_implemented_methods_names = tabular_interfaces_contracts[interface_id].keys()
        runtime_members = member_names(instance)
        assert all(member in runtime_members and str(inspect.signature(getattr(instance, member))) == tabular_interfaces_contracts[interface_id][member] for member in expected_implemented_methods_names)
    return _assert_correct_signatures


@pytest.fixture
def assert_correct_delegate_behaviour(tabular_interfaces_contracts, tabular_operators_reverse):
    def _assert_correct_delegate_behaviour(instance1, instance2):
        instance1_type = type(instance1)
        assert instance1_type == type(instance2)
        assert id(instance1._delegate) != id(instance2._delegate) 

        for function in tabular_interfaces_contracts[tabular_operators_reverse[instance1_type]]:
            assert id(getattr(instance1, function)) != id(getattr(instance2, function))
            assert id(getattr(instance1._delegate, function)) != id(getattr(instance2._delegate, function))
    return _assert_correct_delegate_behaviour


@pytest.mark.parametrize('interface_id', [
    ('retriever'),
    ('iterator'),
    ('mutator'),
])
def test_tabular_interfaces2(interface_id, create_instances, assert_correct_signatures, assert_correct_delegate_behaviour):
    operator_instance1, operator_instance2 = create_instances(*list([interface_id] * 2))

    assert_correct_signatures(operator_instance1)
    assert_correct_delegate_behaviour(operator_instance1, operator_instance2)
