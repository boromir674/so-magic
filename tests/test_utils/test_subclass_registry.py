import pytest


@pytest.fixture
def subclass_registry_metaclass():
    from so_magic.utils import SubclassRegistry
    return SubclassRegistry


def test_subclass_registry(subclass_registry_metaclass):
    class ParentClass(metaclass=subclass_registry_metaclass):
        pass

    assert type(ParentClass) == subclass_registry_metaclass
    assert hasattr(ParentClass, 'subclasses')
    assert hasattr(ParentClass, 'create')
    assert hasattr(ParentClass, 'register_as_subclass')

    assert ParentClass.subclasses == {}

    @ParentClass.register_as_subclass('child1')
    class Child1(ParentClass):
        pass

    assert ParentClass.subclasses['child1'] == Child1

    child1_instance1 = ParentClass.create('child1')

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


    class ParentClass2(metaclass=subclass_registry_metaclass):
        pass

    assert ParentClass.subclasses['child1'] == Child1
    assert ParentClass2.subclasses == {}

    @ParentClass2.register_as_subclass('child2')
    class Child2:
        pass

    assert ParentClass.subclasses['child1'] == Child1
    assert ParentClass2.subclasses['child2'] == Child2

    child1_instance2 = ParentClass2.create('child2')

    assert type(child1_instance2) == Child2
    assert isinstance(child1_instance2, Child2)
    assert not isinstance(child1_instance2, ParentClass2)