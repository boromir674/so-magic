from abc import ABC, abstractmethod
from .engine import DataEngine


class DataBackend(ABC):

    @property
    @abstractmethod
    def commands(self):
        raise NotImplementedError


class Backend(DataBackend, ABC):
    engine_type = DataEngine

    def __init__(self, engine):
        self._engine = engine
        self._commands = {}
    @property
    def commands(self):
        self._commands
    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, engine):
        self._engine = engine

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
