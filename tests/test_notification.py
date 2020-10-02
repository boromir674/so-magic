import pytest

@pytest.fixture
def subject():
    from so_magic.utils import Subject
    return Subject


@pytest.fixture
def observer_class():
    from so_magic.utils import Observer
    return Observer


def test_attrs_sanity():
    import attr

    @attr.s
    class A:
        _observers = attr.ib(init=True, default=[])

    i1 = A()
    i2 = A()
    assert id(i1._observers) == id(i2._observers)  # SOS


def test_attrs_sanity1():
    import attr

    @attr.s
    class A:
        _observers = attr.ib(init=True)
        def add(self, *objects):
            self._observers.extend([_ for _ in objects])
    i1 = A([])
    i2 = A([])
    assert id(i1._observers) != id(i2._observers)
    i1.add('obs1')
    assert i1._observers == ['obs1']
    assert i2._observers == []
    assert id(i1._observers) != id(i2._observers)


def test_observers_sanity_test1(subject):
    subject1 = subject([])
    subject2 = subject([])
    assert id(subject1._observers) != id(subject2._observers)


def test_scenario(subject, observer_class):
# The client code.

    print("------ Scenario 1 ------\n")
    class ObserverA(observer_class):
        def update(self, a_subject) -> None:
            if a_subject.state == 0:
                print("ObserverA: Reacted to the event")

    s1 = subject([])
    o1 = observer_class()
    s1.attach(o1)

    # business logic
    s1.state = 0
    s1.notify()

    print("------ Scenario 2 ------\n")
    # example 2
    class Businessubject(subject):

        def some_business_logic(self) -> None:
            """
            Usually, the subscription logic is only a fraction of what a Subject can
            really do. Subjects commonly hold some important business logic, that
            triggers a notification method whenever something important is about to
            happen (or after it).
            """
            print("\nSubject: I'm doing something important.")
            from random import randrange
            self._state = randrange(0, 10)
            print(f"Subject: My state has just changed to: {self._state}")
            self.notify()

    class ObserverB(observer_class):
        def update(self, a_subject) -> None:
            if a_subject.state == 0 or a_subject.state >= 2:
                print("ObserverB: Reacted to the event")

    s2 = Businessubject([])
    assert id(s1) != id(s2)
    assert id(s1._observers) != id(s2._observers)
    o1, o2 = ObserverA(), ObserverB()
    # s2.attach(o1)
    # s2.attach(o2)
    s2.add(o1, o2)
    # business logic
    print(s2._observers)
    s2.some_business_logic()
    s2.some_business_logic()

    s2.detach(o1)
    s2.some_business_logic()
