from abc import ABC, abstractmethod
from .engine import DataEngine
from green_magic.data.dataset import DatapointsManager

class DataBackend(ABC):
    pass


class Backend(DataBackend, ABC):
    """
        Args:
            engine (DataEngine): a data engine represented as a class object (eg class MyClass: pass)
    """
    def __init__(self, engine):
        self._engine = engine
        self.datapoints_manager = DatapointsManager()

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
