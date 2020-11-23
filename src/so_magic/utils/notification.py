"""Typical subject/observers pattern implementation. You can see this pattern 
mentioned also as event/notification or broadcast/listeners.

* Provides the Observer class, serving as the interface that needs to be implemented by concrete classes; the update method needs to be overrode. Concrete Observers react to the notifications/updates issued by the Subject they had been attached to.
* Provides the Subject class, serving with mechanisms to subscribe/unsubscribe (attach/detach) observers and also with a method to "notify" all subscribers about events.

"""

from abc import ABC, abstractmethod
from typing import List

__all__ = ['Subject', 'Observer']


class Observer(ABC):
    """The Observer interface declares the update method, used by subjects. 
    
    Enables objects to act as "event" listeners; react to "notifications" 
    by executing specific handling logic.
    """
    @abstractmethod
    def update(self, *args, **kwargs) -> None:
        """Receive an update (from a subject); handle an event notification."""
        raise NotImplementedError


class SubjectInterface(ABC):
    """The Subject interface declares a set of methods for managing subscribers.
    
    Enables objects to act as "subjects of observations"; notify the 
    subscribed observers/listeners.
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """Attach an observer to the subject; subscribe the observer."""
        raise NotImplementedError

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """Detach an observer from the subject; unsubscribe the observer."""
        raise NotImplementedError

    @abstractmethod
    def notify(self) -> None:
        """Notify all observers about an event."""
        raise NotImplementedError


class Subject(SubjectInterface):
    """The Subject owns some important state and can notify observers.
    
    Both the _state and _observers attributes can be overrode to accomodate for 
    more complex scenarios."""
    def __new__(cls, *args, **kwargs):
        self_object = super().__new__(cls)
        self_object._observers = []  # type=List[ObserverInterface]
        self_object._state = None
        return self_object

    def add(self, *observers):
        """Subscribe multiple observers at once."""
        self._observers.extend([_ for _ in observers])
    """
    List of subscribers. In more complex scenarios, the list of subscribers can 
    be stored more comprehensively (categorized by event type, etc.).
    """
    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    """
    The subscription management methods.
    """

    def notify(self) -> None:
        """Trigger an update in each subscriber/observer."""
        for observer in self._observers:
            observer.update(self)
