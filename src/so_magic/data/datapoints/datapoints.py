from abc import ABC, abstractmethod
from typing import Iterable
import attr

from .tabular_data_interface import TabularDataInterface


class DatapointsInterface(ABC):
    """Represent multiple data points out of a collection of data.

    Classes implementing this interface, provide to their object instances (eg
    objects created using the classes constructor method) the 'observations'
    property.

    The 'observations' property should hold the information about the
    datapoints.
    """

    @property
    @abstractmethod
    def observations(self) -> Iterable:
        """The collection of datapoints is referenced through this property."""
        raise NotImplementedError


class StructuredDataInterface(ABC):
    """Data points that are expected to have a specific set of attributes.

    Classes implementing this interface, provide to their object instances (eg
    objects created using the classes constructor method) the 'attributes'
    property.

    The 'attributes' property should hold the information about the attributes,
    that each data point (observation) is expected to have.
    """

    @property
    @abstractmethod
    def attributes(self) -> Iterable:
        """The set of attributes is referenced through this property."""
        raise NotImplementedError


class DatapointsFactory:
    """Factory to construct Datapoints objects.

    A class that registers objects (constructors), which can be "called" to return (create) an
    object that implements the DatapointsInterface interface.

    Also, exposes the 'create' factory method that given runtime arguments,
    returns an object that implements the DatapointsInterface interface by
    delegating the creation process to one of the registered constructors.
    """
    constructors = {}

    @classmethod
    def register_constructor(cls, name: str):
        """Register, using a unique name, an object as a "runnable" constructor.

        A decorator method that should decorate a callable" The callable should
        return (create) an object that implements the DatapointsInterface
        interface.

        Args:
            name (str): the name under which to register the "constructor"
        """
        def wrapper(subclass):
            cls.constructors[name] = subclass
            return subclass
        return wrapper

    @classmethod
    def create(cls, name, *args, **kwargs) -> Iterable:
        """Create a Datapoints instance by using a registered "constructor".

        Args:
            name (str): the registered name of the "constructor" to use

        Raises:
            KeyError: happens if the input name is not found in the registry
            DatapointsCreationError: in case the object instantiation operation fails

        Returns:
            Iterable: instance implementing the DatapointsInterface
        """
        if name not in cls.constructors:
            # TODO change to KeyError, because it better indicates the cause of the error
            # In our case a string/key not found in the registry causes the error
            raise KeyError(
                f"Request Engine of type '{name}'; supported are [{', '.join(sorted(cls.constructors.keys()))}]")
        try:
            return cls.constructors[name](*args, **kwargs)
        except Exception as exception:
            raise DatapointsCreationError({
                'exception': exception,
                'name': name,
                'args': args,
                'kwargs': kwargs,
            }) from exception


class DatapointsCreationError(Exception):
    def __init__(self, msg):
        super().__init__(
            f"Exception {str(msg['exception'])}. Datapoints creation failed for constructor {msg['name']}: "
            f"{msg['constructor']}. Args: [{', '.join(f'{i}: {str(_)}' for i, _ in enumerate(msg['args']))}]\nKwargs: "
            f"[{', '.join(f'{k}: {v}' for k, v in msg['kwargs'].items())}]")


@attr.s
@DatapointsFactory.register_constructor('structured-data')
class StructuredData(DatapointsInterface, StructuredDataInterface):
    """Structured data. There are specific attributes/variables per observation.

    Instances of this class represent collections of data (multiple data
    points aka observations). Each data point is expected to hold information
    about the specified attributes and that is why we are dealing with
    structured data/information in contrast to ie image data or sound data.

    Args:
        observations (object): a reference to the actual datapoints object
        attributes (object): a reference to the attributes object
    """
    _observations = attr.ib(init=True)
    _attributes = attr.ib(init=True, converter=lambda input_value: list(input_value))

    # TODO remove property and "promote above attribute '_attributes' to 'attributes'
    @property
    def attributes(self):
        return self._attributes

    @property
    def observations(self):
        return self._observations

    @observations.setter
    def observations(self, observations):
        self._observations = observations


class AbstractTabularData(StructuredData, TabularDataInterface, ABC):
    """Tabular Data with known attributes of interest.

    Classes inheriting from this abstract class, gain both capabilities of structured data
    in terms of their attributes and capabilities of a data table in terms of column, rows, etc.
    """
    def __iter__(self):
        return self.iterrows()


@attr.s
@DatapointsFactory.register_constructor('tabular-data')
class TabularData(AbstractTabularData):
    """Table-like datapoints that are loaded in memory"""

    @property
    def columns(self) -> Iterable:
        pass

    @property
    def rows(self) -> Iterable:
        pass

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
        return iter(set(self.attributes) - set(self.retriever.get_numerical_attributes(self)))

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
