from abc import ABC, abstractmethod
from typing import List, Sequence, AnyStr
import attr
from .dataset import DatapointsManager


class DataBackend(ABC):

    @property
    @abstractmethod
    def commands(self):
        raise NotImplementedError


@attr.s
class Backend(DataBackend, ABC):

    subclasses = {}

    @classmethod
    def register_as_subclass(cls, backend_type):
        def wrapper(subclass):
            cls.subclasses[backend_type] = subclass
            return subclass
        return wrapper

    @classmethod
    def create(cls, backend_type, *args, **kwargs) -> DataBackend:
        if backend_type not in cls.subclasses:
            raise ValueError(f"Request Backend of type '{backend_type}'; supported are [{', '.join(sorted(cls.subclasses.keys()))}]")
        return cls.subclasses[backend_type](*args, **kwargs)

@attr.s
class DataEngine:
    backend = attr.ib(init=True)
    invoker = attr.ib(init=True)
    listeners = attr.ib(init=True, default=[])
    @listeners.validator
    def subscribe_listeners(self, attribute, value):
        """Subscribe listeners to events of Datapoints object construction; whenever the DatapointsFactory constructs a Datapoints object."""
        self.backend.commands.datapoints_factory.subscribe(*value)
    #     for listener in value:
    #         self.backend.commands.datapoints_factory.subscribe(self.datapoints_manager)
    # # datapoints_manager = attr.ib(init=True, default=None)

    # def __attrs_post_init__(self):
    #     self.backend.commands.datapoints_factory.subscribe(self.datapoints_manager)

    @staticmethod
    def default_backend(invoker, listeners):
        """A basic command Invoker and a list of listeners to when the DatapointsFactory constructs a Datapoints object."""
        from .panda_handling import PDBackend
        backend = Backend.create('pandas')
        return DataEngine(backend, invoker, listeners)
