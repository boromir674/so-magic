"""This module is responsible to provide means of creating (instantiating) objects
representing Datapoints collections."""
import logging
import json
from typing import Iterable
import attr
from so_magic.utils import Subject
from .datapoints import DatapointsFactory

logger = logging.getLogger(__name__)


# TODO refactor to a composition (not inheritance) implementation of the below class
# reason is that it will be more evident that this class simply combines the
# features of 2 other classes (Subject & DatapointsFactory) to get the job done
@attr.s
class BroadcastingDatapointsFactory(DatapointsFactory):
    """Creates Datapoints objects and informs its subscribers when that happens.

    A factory class that informs its subscribers when a new object that
    implements the DatapointsInterface is created (following a request).

    Args:
        subject (Subject, optional): the subject of observation; the "thing" that others
                          listen to
    """
    subject: Subject = attr.ib(init=True, default=attr.Factory(Subject))
    name: str = attr.ib(init=False, default='')
    # TODO check if above can be removed, along with self.name = getattr(args[0], 'name', '') in 'create' method

    def create(self, datapoints_factory_type: str, *args, **kwargs) -> Iterable:
        """Create new Datapoints and inform subscribers.

        The factory method that returns a new object of DatapointsInterface, by
        looking at the registered constructors to delegate the object creation.

        Args:
            datapoints_factory_type (str): the name of the "constructor" to use

        Raises:
            RuntimeError: [description]

        Returns:
            Iterable: instance implementing the DatapointsInterface
        """
        self.subject.name = kwargs.pop('id', kwargs.pop('name', kwargs.pop('file_path', '')))
        if kwargs:
            msg = f"Kwargs: [{', '.join(f'{k}: {v}' for k, v in kwargs.items())}]"
            raise RuntimeError("The 'create' method of DatapointsFactory does not support kwargs:", msg)
        self.subject.state = super().create(datapoints_factory_type, *args, **kwargs)
        # logger.debug(f"Created datapoints: {json.dumps({
        #     'datapoints': self.subject.state,
        #     'name': self.subject.name,
        # })}")
        print("Created datapoints: {}".format(json.dumps({
            'datapoints': str(self.subject.state),
            'name': self.subject.name,
        })))
        if args and not hasattr(self, '.name'):
            self.name = getattr(args[0], 'name', '')
        self.subject.notify()
        return self.subject.state
