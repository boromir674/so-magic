"""Defines the DatapointsManager type (class); a centralized facility where all
datapoints objects should arrived and be retrieved from."""
from typing import Iterable, Optional
import json
import logging
import attr
from so_magic.utils import Observer, Subject, ObjectRegistry, ObjectRegistryError

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
    datapoints_registry = attr.ib(converter=lambda ddict: ObjectRegistry(ddict), default=attr.Factory(dict))
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
            raise RuntimeError(f'Subject {subject} with state {str(subject.state)} resulted in an empty string as key. '
                               'We reject the key, since it is going to "query" a dict/hash.')
        if key in self.datapoints_registry:
            raise RuntimeError(f"Attempted to register a new Datapoints object at the existing key '{key}'.")
        self.datapoints_registry.add(key, datapoints_object)
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
            return self.datapoints_registry.get(self._last_key)
        except ObjectRegistryError as non_existent_key_error:
            logger.error('Non existant Datapoints: %s', json.dumps({
                'last-key-used-to-register-datapoints': self._last_key,
                'datapoints-registry-keys': f'[{", ".join(self.datapoints_registry.objects.items())}]',
            }, indent=2))
            raise NonExistantDatapointsError('Requested non existant Datapoints instance. Probable cause is that this '
                                             '(self) DatapointsManager instance has not been notified by a '
                                             'DatapointsFactory') from non_existent_key_error


class NonExistantDatapointsError(Exception): pass
