import pytest


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


def test_retriever_implementation(test_datapoints, built_in_backends):
    built_in_pd_backend = built_in_backends.implementations['pd']
    first_row = built_in_pd_backend['retriever'].row(0, test_datapoints)
    assert list(first_row) == list(test_datapoints.observations.iloc[[0]])
    assert len(list(first_row)) == len(test_datapoints.attributes)
    assert len(list(first_row)) == test_datapoints.nb_columns


# through out the test suite we use the @pytest.mark.xfail decorator to indicate this is expected to fail (since it is a discovered bug).
# when the bug is solved, simply remove the decorator and now you will have a regression test in place!

@pytest.mark.xfail(reason="There is a bug in the built in pandas retriever.get_numerical_attributes method")
def test_retriever_get_numerical_attributes(test_datapoints, built_in_backends):
    built_in_pd_backend = built_in_backends.implementations['pd']
    numerical_attributes = built_in_pd_backend['retriever'].get_numerical_attributes(test_datapoints)
    assert set(numerical_attributes) != {}


def test_iterator_implementation(test_datapoints, built_in_backends):
    built_in_pd_backend = built_in_backends.implementations['pd']
    columns_iterator = built_in_pd_backend['iterator'].itercolumns(test_datapoints)
    import types
    assert type(columns_iterator) == types.GeneratorType
    assert isinstance(columns_iterator, types.GeneratorType)
    

    # assert list(built_in_pd_backend['retriever'].row('Creative', test_datapoints)) == list(test_datapoints)
    # assert list(built_in_pd_backend['retriever'].row('Creative', test_datapoints)) == list(test_datapoints)
    # assert list(built_in_pd_backend['retriever'].row('Creative', test_datapoints)) == list(test_datapoints)
