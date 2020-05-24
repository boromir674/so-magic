from abc import ABC, abstractmethod
from typing import List, Sequence, AnyStr
import attr
from .dataset import Datapoints
from .feature_factory import Feature
from .feature_manager import FeatureManager


class DataBackend(ABC):

    @abstractmethod
    @property
    def commands(self):
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
