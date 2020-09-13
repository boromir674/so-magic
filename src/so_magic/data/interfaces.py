from abc import ABCMeta, abstractmethod, ABC

__all__ = ['TabularIterator', 'TabularRetriever', 'TabularMutator']


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
    @abstractmethod
    def get_numerical_attributes(self, data):
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

class TabularMutator(ABC):
    @abstractmethod
    def add_column(self, *args, **kwargs):
        raise NotImplementedError
