from abc import ABC, abstractmethod
from random import randrange
from typing import List

__all__ = ['Subject', 'ObserverInterface']


class SubjectInterace(ABC):
    """The Subject interface declares a set of methods for managing subscribers.
    Use it to model objects that 'do stuff' and notify observers/listeners/subscribers.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """Attach an observer to the subject."""
        raise NotImplementedError

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """Detach an observer from the subject."""
        raise NotImplementedError

    @abstractmethod
    def notify(self) -> None:
        """Notify all observers about an event."""
        raise NotImplementedError


class Subject(SubjectInterace):
    """The Subject owns some important state and notifies observers when the state changes."""

    _state: int = None

    _observers: List[Observer] = []
    """
    List of subscribers. In real life, the list of subscribers can be stored
    more comprehensively (categorized by event type, etc.).
    """

    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    """
    The subscription management methods.
    """

    def notify(self) -> None:
        """Trigger an update in each subscriber."""

        print("Subject: Notifying observers...")
        for observer in self._observers:
            observer.update(self)


class ObserverInterface(ABC):
    """The Observer interface declares the update method, used by subjects."""

    @abstractmethod
    def update(self, subject: Subject) -> None:
        """Receive update from subject."""
        raise NotImplementedError


"""
Concrete Observers react to the updates issued by the Subject they had been
attached to.
"""


if __name__ == "__main__":
    # The client code.

    class ConcreteSubject(Subject):

        def some_business_logic(self) -> None:
            """
            Usually, the subscription logic is only a fraction of what a Subject can
            really do. Subjects commonly hold some important business logic, that
            triggers a notification method whenever something important is about to
            happen (or after it).
            """
            print("\nSubject: I'm doing something important.")
            self._state = randrange(0, 10)
            print(f"Subject: My state has just changed to: {self._state}")
            self.notify()

    class ConcreteObserverA(ObserverInterface):
        def update(self, subject: Subject) -> None:
            if subject._state < 3:
                print("ConcreteObserverA: Reacted to the event")


    class ConcreteObserverB(ObserverInterface):
        def update(self, subject: Subject) -> None:
            if subject._state == 0 or subject._state >= 2:
                print("ConcreteObserverB: Reacted to the event")

    a_subject = ConcreteSubject()

    observer_a = ConcreteObserverA()
    a_subject.attach(observer_a)

    observer_b = ConcreteObserverB()
    a_subject.attach(observer_b)

    a_subject.some_business_logic()
    a_subject.some_business_logic()

    a_subject.detach(observer_a)

    a_subject.some_business_logic()