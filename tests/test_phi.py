import pytest


@pytest.fixture
def app_phi_function(somagic):
    return somagic._data_manager.phi_class


@pytest.fixture
def assert_function_properties_values():
    def _f(func, expected_name: str, expected_doc: str):
        assert func.__name__ == expected_name
        assert func.__doc__ == expected_doc
    return _f


@pytest.fixture
def assert_class_properties_values():
    def _f(class_obj, expected_name: str, expected_doc: str):
        assert class_obj.__name__ == expected_name
        assert class_obj.__call__.__doc__ == expected_doc
    return _f


@pytest.fixture
def phi_registry(somagic):
    """Magic Phi function registry, listening to registration operations at runtime."""
    return somagic._data_manager.built_phis


@pytest.fixture
def test_phi():
    return {
        'f1': lambda x: x + 1,
        'f2': lambda x: x + 2,
        'f3': lambda x: x + 3,
        'f4': lambda x: x + 4,
        'f5': lambda x: x + 5,
        'f6': lambda x: x + 6,
    }


def test_initial_phi_registry(phi_registry):
    assert phi_registry.registry == {}
    assert 'any-key' not in phi_registry


@pytest.fixture(params=[
    (['pame'], 'f1', 'pame'),
    ([''], 'f2', 'f2_func'),
    ([], 'f3', 'f3_func'),
])
def phi_function_def(request, phi_registry, app_phi_function, test_phi):
    fname = f'{request.param[1]}_func'

    exec(f'def {fname}(x):\n'
         f'    """ela Docstring"""\n'
         f'    return x + {request.param[1][1]}')

    user_function = locals()[fname]
    app_phi_function.register(*request.param[0])(user_function)

    return {
        'func': user_function,
        'expected_key_in_registry': request.param[2],
        'user_defined_function_name': f'{request.param[1]}_func',
        'user_function_code_id': request.param[1],
    }


def test_sc1(phi_function_def, phi_registry, assert_function_properties_values, test_phi):
    assert phi_function_def['expected_key_in_registry'] in phi_registry
    assert_function_properties_values(phi_function_def['func'], f"{phi_function_def['user_defined_function_name']}",
                                      'ela Docstring')
    assert_function_properties_values(phi_registry.get(phi_function_def['expected_key_in_registry']),
                                      phi_function_def['user_defined_function_name'], 'ela Docstring')
    assert phi_registry.get(phi_function_def['expected_key_in_registry'])(1) == \
           test_phi[phi_function_def['user_function_code_id']](1)


@pytest.fixture(params=[
    (['edw'], 'f1', 'edw'),
    ([''], 'f2', 'f2'),
    ([], 'f3', 'f3'),
])
def phi_class_def(request, phi_registry, app_phi_function, test_phi):

    def __call__(self, data, **kwargs):
        """Add a small integer to the input number.

        Args:
            data ([type]): numerical value

        Returns:
            [type]: the result of the addition
        """
        return test_phi[(request.param[1])](data)

    class_obj = type(request.param[1], (object,), {
        '__call__': __call__,
    })
    app_phi_function.register(*request.param[0])(class_obj)

    return {
        'func': class_obj,
        'expected_key_in_registry': request.param[2],
        'expected_phi_logic': request.param[1],
    }


def test_sc2(phi_class_def, phi_registry, assert_class_properties_values, test_phi):
    assert phi_class_def['expected_key_in_registry'] in phi_registry
    assert_class_properties_values(phi_class_def['func'], phi_class_def['expected_phi_logic'],
                                   phi_class_def['func'].__call__.__doc__)
    assert_class_properties_values(phi_registry.get(phi_class_def['expected_key_in_registry']),
                                   phi_class_def['expected_phi_logic'], phi_class_def['func'].__call__.__doc__)
    assert phi_registry.get(phi_class_def['expected_key_in_registry'])(1) == \
           test_phi[phi_class_def['expected_phi_logic']](1)


#     def gg(x):
#         return x
#
#     test_value = 1
#     assert gg(test_value) == test_value
#     assert phi_registry.get('gg')(test_value) == test_value * 2
#
#     with pytest.raises(registering_phi_at_the_same_key_error):
#         PhiFunction.register('')(gg)
#
#     assert phi_registry.get('gg')(test_value) == test_value * 2
