from abc import ABC, abstractmethod
import os
import attr

from green_magic.utils import Observer, Subject


@attr.s(str=True, repr=True)
class Dataset:
    datapoints = attr.ib(init=True)
    name = attr.ib(init=True, default=None)

    _features = attr.ib(init=True, default=[])
    handler = attr.ib(init=True, default=None)
    size = attr.ib(init=False, default=attr.Factory(lambda self: len(self.datapoints) if self.datapoints else 0, takes_self=True))

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, features):
        self._features = features


class DatapointsInterface(ABC):
    """The Datapoints interface gives access to the 'observations' property."""
    @property
    @abstractmethod
    def observations(self):
        raise NotImplementedError

class StructuredDataInterface(ABC):
    @property
    @abstractmethod
    def attributes(self):
        raise NotImplementedError


class DatapointsFactory:
    constructors = {}

    @classmethod
    def register_constructor(cls, name):
        def wrapper(subclass):
            cls.constructors[name] = subclass
            return subclass
        return wrapper

    @classmethod
    def create(cls, name, *args, **kwargs) -> DatapointsInterface:
        if name not in cls.constructors:
            raise ValueError(
                f"Request Engine of type '{name}'; supported are [{', '.join(sorted(cls.constructors.keys()))}]")
        try:
            return cls.constructors[name](*args, **kwargs)
        except TypeError as e:
            print(f"Datapoints creation failed. Args: [{', '.join(f'{i}: {str(_)}' for i, _ in enumerate(args))}]")
            print(f"Kwargs: [{', '.join(f'{k}: {v}' for k, v in kwargs.items())}]")
            print(e)
            import sys
            sys.exit(1)


class BroadcastingDatapointsFactory(DatapointsFactory):
    subject = Subject([])

    @classmethod
    def create(cls, name, *args, **kwargs) -> DatapointsInterface:
        cls.subject.state = super().create(name, *args, **kwargs)
        cls.subject.name = kwargs.get('id', kwargs.get('name', ''))
        if args and not hasattr(cls, '.name'):
            cls.name = getattr(args[0], 'name', '')
        cls.subject.notify()
        return cls.subject.state


@attr.s
@DatapointsFactory.register_constructor('structured-data')
class StructuredData(DatapointsInterface, StructuredDataInterface):
    """Structured data. There are specific attributes/variables per observation.

    Args:
        observations (object): a reference to an object that encapsulates structured data
    """
    _observations = attr.ib(init=True)
    _attributes = attr.ib(init=True, converter=lambda input_value: [x for x in input_value])

    @property
    def attributes(self):
        return self._attributes

    @property
    def observations(self):
        return self._observations

@attr.s
@DatapointsFactory.register_constructor('tabular-data')
class TabularData(StructuredData):
    """Table-like datapoints that are loaded in memory"""
    retriever = attr.ib(init=True)
    iterator = attr.ib(init=True)
    mutator = attr.ib(init=True)

    @property
    def attributes(self):
        return self.iterator.columnnames(self)

    def column(self, identifier):
        return self.retriever.column(identifier, self)

    def row(self, identifier):
        return self.retriever.row(identifier, self)

    def get_numerical_attributes(self):
        return self.retriever.get_numerical_attributes(self)

    def get_categorical_attributes(self):
        return iter(set(self.attributes) - set([_ for _ in self.retriever.get_numerical_attributes(self)]))

    @property
    def nb_columns(self):
        return self.retriever.nb_columns(self)

    @property
    def nb_rows(self):
        return self.retriever.nb_rows(self)

    def __len__(self):
        return self.retriever.nb_rows(self)

    def __iter__(self):
        return self.iterator.iterrows(self)

    def iterrows(self):
        return self.iterator.iterrows(self)

    def itercolumns(self):
        return self.iterator.itercolumns(self)


@attr.s
class DatapointsManager(Observer):
    datapoints_objects = attr.ib(init=True, default={})
    _last_key = attr.ib(init=False, default='')

    def update(self, subject: Subject):
        datapoints_object = subject.state
        key = getattr(subject, 'name', '')
        if key in self.datapoints_objects:
            raise RuntimeError(f"Attempted to register a new Datapoints object at the existing key '{key}'.")
        self.datapoints_objects[key] = datapoints_object
        self._last_key = key

    @property
    def state(self):
        return self._last_key

    @property
    def datapoints(self):
        try:
            return self.datapoints_objects[self._last_key]
        except KeyError as e:
            print(f"{e}. Requested datapoints with id '{self._last_key}', but was not found in registered [{', '.join(_ for _ in self.datapoints_objects.keys())}]")
