from abc import ABC
import attr

from green_magic.data.interfaces import TabularRetriever, TabularIterator, TabularMutator


class EngineTabularRetriever(TabularRetriever, ABC):

    subclasses = {}

    @classmethod
    def register_as_subclass(cls, backend_type):
        def wrapper(subclass):
            cls.subclasses[backend_type] = subclass
            return subclass
        return wrapper

    @classmethod
    def create(cls, backend_type, *args, **kwargs) -> TabularRetriever:
        if backend_type not in cls.subclasses:
            raise ValueError(
                f"Requested TabularRetriever of type '{backend_type}'; supported are [{', '.join(sorted(cls.subclasses.keys()))}]")
        return cls.subclasses[backend_type](*args, **kwargs)


class EngineTabularIterator(TabularIterator, ABC):
    subclasses = {}

    @classmethod
    def register_as_subclass(cls, backend_type):
        def wrapper(subclass):
            cls.subclasses[backend_type] = subclass
            return subclass

        return wrapper

    @classmethod
    def create(cls, backend_type, *args, **kwargs) -> TabularRetriever:
        if backend_type not in cls.subclasses:
            raise ValueError(
                f"Requested TabularIterator of type '{backend_type}'; supported are [{', '.join(sorted(cls.subclasses.keys()))}]")
        return cls.subclasses[backend_type](*args, **kwargs)


class EngineTabularMutator(TabularMutator, ABC):
    subclasses = {}

    @classmethod
    def register_as_subclass(cls, backend_type):
        def wrapper(subclass):
            cls.subclasses[backend_type] = subclass
            return subclass

        return wrapper

    @classmethod
    def create(cls, backend_type, *args, **kwargs) -> TabularRetriever:
        if backend_type not in cls.subclasses:
            raise ValueError(
                f"Requested TabularMutator of type '{backend_type}'; supported are [{', '.join(sorted(cls.subclasses.keys()))}]")
        return cls.subclasses[backend_type](*args, **kwargs)


@attr.s
class EngineSpecifications:
    name_abbreviation = attr.ib(init=True)
    name = attr.ib(init=True, default=attr.Factory(lambda self: self.name_abbreviation, takes_self=True))

    def __call__(self, *args, **kwargs):
        engine = args[0]
        engine.retriever = EngineTabularRetriever.subclasses[self.name_abbreviation]
        engine.iterator = EngineTabularIterator.subclasses[self.name_abbreviation]
        engine.mutator = EngineTabularMutator.subclasses[self.name_abbreviation]

    @classmethod
    def from_dict(cls, a_dict):
        return EngineSpecifications(a_dict['id'], a_dict.get('name', a_dict['id']))
