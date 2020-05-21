from abc import ABC, abstractmethod
from typing import List, Sequence, AnyStr
from .dataset import Datapoints
from .feature_factory import Feature


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
    def check_features(self, dataset: Dataset, features: Sequence[Feature]):
        raise NotImplementedError

    @abstractmethod
    def encodable_features(self, dataset: Dataset) -> List[Feature]:
        raise NotImplementedError

    @property
    @abstractmethod
    def features_factory(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def commands_manager(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def computing(self):
        raise NotImplementedError


class Backend(DataBackend):
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
            raise ValueError('Bad "Data Backend type" type \'{}\''.format(backend_type))
        return cls.subclasses[backend_type](*args, **kwargs)

    @abc.abstractmethod
    def datapoints_from_file(self, file_path: AnyStr) -> Datapoints:
        raise NotImplementedError

    @abc.abstractmethod
    def check_features(self, dataset: Dataset, features: Sequence[Feature]):
        raise NotImplementedError

    @abc.abstractmethod
    def encodable_features(self, dataset: Dataset) -> List[Feature]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def features_factory(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def commands_manager(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def computing(self):
        raise NotImplementedError