import pytest


@pytest.fixture
def subclass_registry_metaclass():
    from so_magic.utils import SubclassRegistry
    return SubclassRegistry


@pytest.fixture
def register_class(subclass_registry_metaclass):
    def _register_class(subclass_id: str, inherit=False):
        class ParentClass(metaclass=subclass_registry_metaclass):
            pass

        if inherit:
            @ParentClass.register_as_subclass(subclass_id)
            class Child(ParentClass):
                pass
        else:
            @ParentClass.register_as_subclass(subclass_id)
            class Child:
                pass

        child_instance = ParentClass.create(subclass_id)

        return {'class_registry': ParentClass, 'child': Child, 'child_instance': child_instance}
    return _register_class


@pytest.fixture
def use_metaclass(register_class, assert_correct_metaclass_behaviour):
    is_instance = {True: lambda classes: isinstance(classes['child_instance'], classes['class_registry']),
                False: lambda classes: not isinstance(classes['child_instance'], classes['class_registry'])}
    def _use_metaclass_in_scenario(subclass_id: str, inherit=False):
        classes = register_class(subclass_id, inherit=inherit)
        assert_correct_metaclass_behaviour(classes, subclass_id)
        assert is_instance[inherit]
        return classes['child_instance'], classes['child'], classes['class_registry']
    return _use_metaclass_in_scenario


@pytest.fixture
def assert_correct_metaclass_behaviour():
    def assert_metaclass_behaviour(classes, subclass_id):
        assert classes['class_registry'].subclasses[subclass_id] == classes['child']
        assert type(classes['child_instance']) == classes['child']
        assert isinstance(classes['child_instance'], classes['child'])
    return assert_metaclass_behaviour


def test_metaclass_usage(subclass_registry_metaclass):
    class ParentClass(metaclass=subclass_registry_metaclass):
        pass

    assert type(ParentClass) == subclass_registry_metaclass
    assert hasattr(ParentClass, 'subclasses')
    assert hasattr(ParentClass, 'create')
    assert hasattr(ParentClass, 'register_as_subclass')
    assert ParentClass.subclasses == {}


def test_subclass_registry(use_metaclass):
    child1_instance1, Child1, ParentClass = use_metaclass('child1', inherit=True)

    non_existent_identifier = 'child2'

    exception_message_regex = \
        f'Bad "{str(ParentClass.__name__)}" subclass request; requested subclass with identifier ' \
        f'{non_existent_identifier}, but known identifiers are ' \
        rf'\[{", ".join(subclass_identifier for subclass_identifier in ParentClass.subclasses.keys())}\]'

    with pytest.raises(ValueError, match=exception_message_regex):
        ParentClass.create(non_existent_identifier)

    child1_instance2, Child2, ParentClass2 = use_metaclass('child2', inherit=False)
    assert ParentClass.subclasses['child1'] == Child1
