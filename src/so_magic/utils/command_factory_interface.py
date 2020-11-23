"""This module is responsible to define an interface to construct Command objects (instances of the Command class)."""
from abc import ABC, abstractmethod
from so_magic.utils import Command


class CommandFactoryInterface(ABC):
    """Define a way to create objects of type Command.

    Classes implementing this interface define a way to construct (initialize) new Command objects (class instances).
    """
    @abstractmethod
    def construct(self, *args, **kwargs) -> Command:
        """Construct a new Command object (new class instance) that can be executed.

        Returns:
            Command: the command object (instance)
        """
        raise NotImplementedError


class CommandFactoryType(type):
    def __new__(mcs, *args, **kwargs):
        x = super().__new__(mcs, *args, **kwargs)
        x.subclasses = {}
        return x

    def register_as_subclass(cls, factory_type):
        def wrapper(subclass):
            cls.subclasses[factory_type] = subclass
            return subclass
        return wrapper

    def create(cls, factory_type, *args, **kwargs):
        if factory_type not in cls.subclasses:
            raise ValueError('Bad "Factory type" \'{}\''.format(factory_type))
        return cls.subclasses[factory_type](*args, **kwargs)
