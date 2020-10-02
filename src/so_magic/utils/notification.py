from abc import ABC, abstractmethod
from typing import List

__all__ = ['Subject', 'Observer']


class ObserverInterface(ABC):
    """The Observer interface declares the update method, used by subjects. Whenever an 'event' happens the update
    callback executes."""
    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """Receive update from subject."""
        raise NotImplementedError


class SubjectInterface(ABC):
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


class Subject(SubjectInterface):
    """The Subject owns some important state and notifies observers when the state changes. Both the _state and _observers
    attributes can be overriden to accomodate for more complex scenarios."""
    def __new__(cls, *args, **kwargs):
        self_object = super().__new__(cls)
        self_object._observers = []  # type=List[ObserverInterface]
        self_object._state = None
        return self_object

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
