from abc import ABC, abstractmethod
from typing import List, Sequence, AnyStr
import attr
from .dataset import Datapoints
from .feature_factory import Feature
from .feature_manager import FeatureManager


class AbstractObsevationsFactory(ABC):
    @abstractmethod
    def from_file(self, file_path: AnyStr):
        raise NotImplementedError

    @abstractmethod
    def from_pickle(self, file_path: AnyStr):
        raise NotImplementedError


class DataBackend(ABC):
    @abstractmethod
    def observations_from_file(self, file_path: AnyStr) -> Datapoints:
        raise NotImplementedError

    @abstractmethod
    @property
    def features_manager(self):
        raise NotImplementedError

    @abstractmethod
    @property
    def commands_manager(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def computer(self):
        raise NotImplementedError

@attr.s
class Backend(DataBackend, ABC):
    features_manager = attr.ib(init=True, default=FeatureManager)

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
            raise ValueError("Bad 'Data Backend' of type '{}'".format(backend_type))
        return cls.subclasses[backend_type](*args, **kwargs)

    @property
    def features_manager(self):
        return self.features_manager
