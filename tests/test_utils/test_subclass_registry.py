import pytest


@pytest.fixture
def subclass_registry_metaclass():
    from so_magic.utils import SubclassRegistry
    return SubclassRegistry


@pytest.fixture
def assert_correct_class_creation(subclass_registry_metaclass):
    def assert_class_creation(user_class):
        assert type(user_class) == subclass_registry_metaclass
        assert hasattr(user_class, 'subclasses')
        assert hasattr(user_class, 'create')
        assert hasattr(user_class, 'register_as_subclass')
        assert user_class.subclasses == {}
    return assert_class_creation


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
def usage_with_subclass(register_class, assert_correct_metaclass_behaviour):
    def parent_n_child_classes(subclass_id: str):
        classes = register_class(subclass_id, inherit=True)

        assert_correct_metaclass_behaviour(classes, subclass_id)
        assert isinstance(classes['child_instance'], classes['class_registry'])

        return classes['child_instance'], classes['child'], classes['class_registry']
    return parent_n_child_classes


@pytest.fixture
def plain_usage(register_class, assert_correct_metaclass_behaviour):
    def parent_n_child_classes(subclass_id: str):
        classes = register_class(subclass_id, inherit=False)

        assert_correct_metaclass_behaviour(classes, subclass_id)
        assert not isinstance(classes['child_instance'], classes['class_registry'])

        return classes['child_instance'], classes['child'], classes['class_registry']
    return parent_n_child_classes


@pytest.fixture
def assert_correct_metaclass_behaviour():
    def assert_metaclass_behaviour(classes, subclass_id):
        assert classes['class_registry'].subclasses[subclass_id] == classes['child']
        assert type(classes['child_instance']) == classes['child']
        assert isinstance(classes['child_instance'], classes['child'])
    return assert_metaclass_behaviour


def test_metaclass_usage(subclass_registry_metaclass, assert_correct_class_creation):
    class ParentClass(metaclass=subclass_registry_metaclass):
        pass

    assert_correct_class_creation(ParentClass)


def test_subclass_registry(usage_with_subclass, plain_usage):
    child1_instance1, Child1, ParentClass = usage_with_subclass('child1')

    non_existent_identifier = 'child2'

    exception_message_regex = \
        f'Bad "{str(ParentClass.__name__)}" subclass request; requested subclass with identifier ' \
        f'{non_existent_identifier}, but known identifiers are ' \
        rf'\[{", ".join(subclass_identifier for subclass_identifier in ParentClass.subclasses.keys())}\]'

    with pytest.raises(ValueError, match=exception_message_regex):
        ParentClass.create(non_existent_identifier)

    child1_instance2, Child2, ParentClass2 = plain_usage('child2')
    assert ParentClass.subclasses['child1'] == Child1
