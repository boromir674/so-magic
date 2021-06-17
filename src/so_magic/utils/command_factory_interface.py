"""This module is responsible to define an interface to construct Command objects (instances of the Command class)."""
from abc import ABC, abstractmethod
from .command_interface import CommandInterface


class CommandFactoryInterface(ABC):
    """Define a way to create objects of type Command.

    Classes implementing this interface define a way to construct (initialize) new Command objects (class instances).
    """
    @abstractmethod
    def construct(self, *args, **kwargs) -> CommandInterface:
        """Construct a new Command object (new class instance) that can be executed.

        Returns:
            Command: the command object (instance)
        """
        raise NotImplementedError
