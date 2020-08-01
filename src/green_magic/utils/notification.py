from abc import ABC, abstractmethod
from typing import List
import attr

__all__ = ['Subject', 'Observer']


class ObserverInterface(ABC):
    """The Observer interface declares the update method, used by subjects. Whenever an 'event' happens the update
    callback executes."""
    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """Receive update from subject."""
        raise NotImplementedError


class SubjectInterace(ABC):
    """The Subject interface declares a set of methods for managing subscribers.
    Use it to model objects as "subjects of observations" (notify observers/listeners/subscribers).
    """

    @abstractmethod
    def attach(self, observer: ObserverInterface) -> None:
        """Attach an observer to the subject."""
        raise NotImplementedError

    @abstractmethod
    def detach(self, observer: ObserverInterface) -> None:
        """Detach an observer from the subject."""
        raise NotImplementedError

    @abstractmethod
    def notify(self) -> None:
        """Notify all observers about an event."""
        raise NotImplementedError

@attr.s
class Subject(SubjectInterace):
    """The Subject owns some important state and notifies observers when the state changes. Both the _state and _observers
    attributes can be overriden to accomodate for more complex scenarios."""
    # State implementation
    _state = attr.ib(init=False, default=None, type=int)
    _observers = attr.ib(init=False, default=[], type=List[ObserverInterface])
    # Subscribers implementation
    # _observers: List[ObserverInterface] = []
    def add(self, *observers):
        self._observers.extend([_ for _ in observers])
    """
    List of subscribers. In real life, the list of subscribers can be stored
    more comprehensively (categorized by event type, etc.).
    """
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    def attach(self, observer: ObserverInterface) -> None:
        self._observers.append(observer)

    def detach(self, observer: ObserverInterface) -> None:
        self._observers.remove(observer)

    """
    The subscription management methods.
    """

    def notify(self) -> None:
        """Trigger an update in each subscriber/observer."""
        for observer in self._observers:
            observer.update(self)

"""
Concrete Observers react to the updates issued by the Subject they had been
attached to.
"""
class Observer(ObserverInterface):
    def update(self, subject: Subject) -> None:
        pass


if __name__ == "__main__":
    # The client code.
    # example 1
    print("------ Scenario 1 ------\n")
    class ObserverA(Observer):
        def update(self, subject: Subject) -> None:
            if subject.state == 0:
                print("ObserverA: Reacted to the event")

    s1 = Subject()
    o1 = ObserverA()
    s1.attach(o1)

    # business logic
    print(s1._observers)
    s1.state = 0
    s1.notify()

    print("------ Scenario 2 ------\n")
    # example 2
    class Businessubject(Subject):

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

    class ObserverB(Observer):
        def update(self, subject: Subject) -> None:
            if subject.state == 0 or subject.state >= 2:
                print("ObserverB: Reacted to the event")

    s2 = Businessubject()
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
