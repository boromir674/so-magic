import pytest


@pytest.fixture
def tabular_operators():
    from so_magic.data.backend.panda_handling.df_backend import PDTabularRetriever, PDTabularIterator, PDTabularMutator
    operators = {
        'retriever': {
            'class': PDTabularRetriever,
            'interface': {
                'column': '(identifier, data)',
                'row': '(identifier, data)',
                'nb_columns': '(data)',
                'nb_rows': '(data)',
                'get_numerical_attributes': '(data)',
            }
        },
        'iterator': {
            'class': PDTabularIterator,
            'interface': {
                'columnnames': '(data)',
                'itercolumns': '(data)',
                'iterrows': '(data)',
            },
        },
        'mutator': {
            'class': PDTabularMutator,
            'interface': {
                'add_column': '(datapoints, values, new_attribute, **kwargs)',
            },
        },
    }
    return {
        'operators': operators,
        'reverse_dict': {operator_dict['class']: key for key, operator_dict in operators.items()},
    }


@pytest.fixture
def assert_correct_signatures(tabular_operators):
    def _assert_correct_signatures(instance):
        interface_id = tabular_operators['reverse_dict'][type(instance)]
        expected_implemented_methods_names = tabular_operators['operators'][interface_id]['interface'].keys()
        assert all(callable(getattr(instance, member, None)) for member in expected_implemented_methods_names)
    return _assert_correct_signatures


@pytest.fixture
def assert_correct_delegate_behaviour(tabular_operators):
    def _assert_correct_delegate_behaviour(instance1, instance2):
        instance1_type = type(instance1)
        instance1_operator_id = tabular_operators['reverse_dict'][instance1_type]
        assert instance1_type == type(instance2)
        assert id(instance1._delegate) != id(instance2._delegate)
        for function in tabular_operators['operators'][instance1_operator_id]['interface']:
        # for function in tabular_interfaces_contracts[tabular_operators_reverse[instance1_type]]:
            assert id(getattr(instance1, function)) != id(getattr(instance2, function))
            assert id(getattr(instance1._delegate, function)) != id(getattr(instance2._delegate, function))
    return _assert_correct_delegate_behaviour


@pytest.mark.parametrize('interface_id', [
    ('retriever'),
    ('iterator'),
    ('mutator'),
])
def test_tabular_interfaces2(interface_id, tabular_operators, assert_correct_signatures, assert_correct_delegate_behaviour):
    operator_instance1, operator_instance2 = tuple(tabular_operators['operators'][_interface_id]['class']() for _interface_id in [interface_id] * 2)

    assert_correct_signatures(operator_instance1)
    assert_correct_delegate_behaviour(operator_instance1, operator_instance2)
