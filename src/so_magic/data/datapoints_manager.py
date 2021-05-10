"""Defines the DatapointsManager type (class); a centralized facility where all
datapoints objects should arrived and be retrieved from."""
from typing import Iterable, Optional
import logging
import attr
from so_magic.utils import Observer, Subject

logger = logging.getLogger(__name__)


@attr.s
class DatapointsManager(Observer):
    """Manage operations revolved around datapoints collection objects.

    Instances of this class are able to monitor (listener/observer pattern) the creation of
    datapoints collection objects and store them in a dictionary structure.
    They also provide retrieval methods to the client to "pick up" a datapoints object.

    Args:
        datapoints_objects (dict, optional): the initial structure that stores datapoints objects
    """
    datapoints_objects = attr.ib(init=True, default={})
    _last_key = attr.ib(init=False, default='')

    def update(self, subject: Subject):
        """Update our state based on the event/observation captured/made.

        Stores the datapoints object observed in a dictionary using a the Subject
        name attribute as key.

        Args:
            subject (Subject): the subject object observed; it acts as an event

        Raises:
            RuntimeError: in case there is no 'name' attribute on the subject or if it is an empty string ''
            RuntimeError: in case the 'name' attribute on the subject has already been used to store a datapoints object
        """
        datapoints_object = subject.state
        key = getattr(subject, 'name', '')
        if key == '':
            raise RuntimeError(f'Subject {subject} with state {str(subject.state)} resulted in an empty string as key.'
                               f'We reject the key, since it is going to "query" a in dict/hash).')
        if key in self.datapoints_objects:
            raise RuntimeError(f"Attempted to register a new Datapoints object at the existing key '{key}'.")
        self.datapoints_objects[key] = datapoints_object
        self._last_key = key

    @property
    def state(self):
        """The latest (most recent) key used to store a datapoints object.

        Returns:
            str: the key under which we stored a datapoints object last time
        """
        return self._last_key

    @property
    def datapoints(self) -> Optional[Iterable]:  # indicates that the method can return an Iterable or None types
        """The most recently stored datapoints object.

        Returns:
            Optional[Iterable]: the reference to the datapoints object
        """
        try:
            return self.datapoints_objects[self._last_key]
        except KeyError as exception:
            logger.error("%s . Requested datapoints with id '%s', but was not found in registered [%s]",
                         exception, self._last_key, {', '.join(_ for _ in self.datapoints_objects.keys())})
