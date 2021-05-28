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
def usage_with_subclass(subclass_registry_metaclass, assert_correct_metaclass_behaviour):
    def parent_n_child_classes(subclass_id: str):
        class ParentClass(metaclass=subclass_registry_metaclass):
            pass

        @ParentClass.register_as_subclass(subclass_id)
        class Child1(ParentClass):
            pass

        child1_instance1 = ParentClass.create(subclass_id)

        assert_correct_metaclass_behaviour(ParentClass, subclass_id, Child1, child1_instance1)
        assert isinstance(child1_instance1, ParentClass)

        return child1_instance1, Child1, ParentClass
    return parent_n_child_classes


@pytest.fixture
def plain_usage(subclass_registry_metaclass, assert_correct_metaclass_behaviour):
    def parent_n_child_classes(subclass_id: str):
        class ParentClass2(metaclass=subclass_registry_metaclass):
            pass

        @ParentClass2.register_as_subclass()
        class Child2:
            pass

        child1_instance2 = ParentClass2.create(subclass_id)

        assert_correct_metaclass_behaviour(ParentClass2, subclass_id, Child2, child1_instance2)
        assert not isinstance(child1_instance2, ParentClass2)

        return child1_instance2, Child2, ParentClass2
    return parent_n_child_classes


@pytest.fixture
def assert_correct_metaclass_behaviour():
    def assert_metaclass_behaviour(metaclass_user, subclass_id, subclass, subclass_instance):
        assert metaclass_user.subclasses[subclass_id] == subclass
        assert type(subclass_instance) == subclass
        assert isinstance(subclass_instance, subclass)
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
