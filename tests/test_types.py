import pytest


@pytest.fixture
def variable_class_name_regex():
    def _variable_class_name_regex(variable_code_name):
        import re
        return re.compile(rf'\w*{variable_code_name}\w*')
    return _variable_class_name_regex


@pytest.fixture
def discovered_types():
    import importlib
    import inspect
    return {name: cls for name, cls in inspect.getmembers(
        importlib.import_module("so_magic.data.variables.types"), inspect.isclass)}


@pytest.fixture
def find_matches(discovered_types, variable_class_name_regex):
    return lambda variable_code_name: [_class_name for match, _class_name in ((variable_class_name_regex(
        variable_code_name).match(class_name.lower()), class_name) for class_name in discovered_types.keys())
                                      if bool(match)]


@pytest.fixture
def expected_number_of_matches():
    # doto: improve below dict by using default dict
    d = {'': lambda discovered_types: len(discovered_types)}

    def _expected_number_of_matches(parent_code_name):
        return d.get(parent_code_name, lambda discovered_types: 1)
    return _expected_number_of_matches


@pytest.fixture(params=[
    ['categorical', ''],
    ['nominal', 'categorical'],
    ['nominal', 'categorical'],
    ['numerical', ''],
    ['interval', 'numerical'],
    ['ratio', 'numerical'],
])
def variables_to_test(request, find_matches):
    return request.param, find_matches(request.param[0])


@pytest.fixture
def check_node(discovered_types, find_matches, expected_number_of_matches):
    def _check_node(class_name, parent_code_name):
        variable_type_class = discovered_types[class_name]
        # find immediate ancestors
        variable_type_superclasses = variable_type_class.__bases__
        # building the data
        matches = find_matches(parent_code_name)
        assert len(matches) == expected_number_of_matches(parent_code_name)(discovered_types)
        # we expect that the class matching the 'parent_code_name' will be a superclass of the variable type class
        assert matches[0] in [_.__name__ for _ in variable_type_superclasses]
    return _check_node


def test_types_follow_taxonomy(check_node, variables_to_test):
    assert len(variables_to_test[1]) == 1
    check_node(variables_to_test[1][0], variables_to_test[0][1])
