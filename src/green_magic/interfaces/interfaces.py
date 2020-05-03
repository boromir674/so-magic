from abc import ABCMeta, abstractmethod, ABC

__all__ = ['Normalization', 'Discretization', 'Encoding', 'Visitor', 'Component']


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

#########################################################################


class Visitor(metaclass=ABCMeta):
    """
    The Visitor Interface declares a set of visiting methods that correspond to
    component classes. The signature of a visiting method allows the visitor to
    identify the exact class of the component that it's dealing with.
    """
    pass

class Component(ABC):
    """
    The Component interface declares an `accept` method that should take the
    base visitor interface as an argument.
    """

    @abstractmethod
    def accept(self, visitor: Visitor) -> None:
        raise NotImplementedError
