from abc import ABCMeta, abstractmethod, ABC

__all__ = ['TabularIterator', 'TabularRetriever', 'Normalization', 'Discretization', 'Encoding', 'Visitor', 'Component']


class TabularRetriever(ABC):
    @abstractmethod
    def column(self, identifier, data):
        raise NotImplementedError
    @abstractmethod
    def row(self, identifier, data):
        raise NotImplementedError
    @abstractmethod
    def nb_columns(self, data):
        raise NotImplementedError
    @abstractmethod
    def nb_rows(self, data):
        raise NotImplementedError


class TabularIterator(ABC):
    @abstractmethod
    def iterrows(self, data):
        raise NotImplementedError
    @abstractmethod
    def itercolumns(self, data):
        raise NotImplementedError
    @abstractmethod
    def columnnames(self, data):
        raise NotImplementedError


class Normalization(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'normalize') and callable(subclass.normalize)

    @abstractmethod
    def normalize(self, *args, **kwargs):
        raise NotImplementedError


class Discretization(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'discretize') and callable(subclass.discretize)

    @abstractmethod
    def discretize(self, *args, **kwargs):
        raise NotImplementedError


class Encoding(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return hasattr(subclass, 'encode') and callable(subclass.encode)

    @abstractmethod
    def encode(self, *args, **kwargs):
        raise NotImplementedError