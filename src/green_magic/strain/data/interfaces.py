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