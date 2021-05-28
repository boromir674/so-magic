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


def test_metaclass_usage(subclass_registry_metaclass, assert_correct_class_creation):
    class ParentClass(metaclass=subclass_registry_metaclass):
        pass

    assert_correct_class_creation(ParentClass)


@pytest.fixture
def usage_with_subclass(subclass_registry_metaclass):
    def parent_n_child_classes():
        class ParentClass(metaclass=subclass_registry_metaclass):
            pass
        @ParentClass.register_as_subclass('child1')
        class Child1(ParentClass):
            pass

        child1_instance1 = ParentClass.create('child1')
        return child1_instance1, Child1, ParentClass
    return parent_n_child_classes


@pytest.fixture
def plain_usage(subclass_registry_metaclass):
    def parent_n_child_classes():
        class ParentClass2(metaclass=subclass_registry_metaclass):
            pass

        @ParentClass2.register_as_subclass('child2')
        class Child2:
            pass

        child1_instance2 = ParentClass2.create('child2')
        return child1_instance2, Child2, ParentClass2
    return parent_n_child_classes


def test_subclass_registry(usage_with_subclass, plain_usage):
    child1_instance1, Child1, ParentClass = usage_with_subclass()

    assert ParentClass.subclasses['child1'] == Child1

    assert type(child1_instance1) == Child1
    assert isinstance(child1_instance1, Child1)
    assert isinstance(child1_instance1, ParentClass)

    non_existent_identifier = 'child2'

    exception_message_regex = \
        f'Bad "{str(ParentClass.__name__)}" subclass request; requested subclass with identifier ' \
        f'{non_existent_identifier}, but known identifiers are ' \
        rf'\[{", ".join(subclass_identifier for subclass_identifier in ParentClass.subclasses.keys())}\]'

    with pytest.raises(ValueError, match=exception_message_regex):
        ParentClass.create(non_existent_identifier)


    child1_instance2, Child2, ParentClass2 = plain_usage()

    assert ParentClass.subclasses['child1'] == Child1
    assert ParentClass2.subclasses['child2'] == Child2

    assert type(child1_instance2) == Child2
    assert isinstance(child1_instance2, Child2)
    assert not isinstance(child1_instance2, ParentClass2)
