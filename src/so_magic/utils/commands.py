from abc import ABC, abstractmethod
import copy
from typing import List

__all__ = ['Command', 'Invoker', 'CommandHistory', 'CommandInterface']


class CommandInterface(ABC):
    """A class implementing this interface can act as a standalone command, encapsulating all logic and data needed."""
    @abstractmethod
    def execute(self) -> None:
        """Call this method to execute the command.
        """
        raise NotImplementedError

class AbstractCommand(CommandInterface, ABC):
    """An abstract implementation of the Command Interface. The assumption is that the command involves a 'reveiver' object
    (of arbitrary type) acting as an 'oracle' on the application.

    Args:
        receiver (object): an object that is actually executing/receiving the command; usually holds the callback function/code
    """
    def __init__(self, receiver):
        self._receiver = receiver


class BaseCommand(AbstractCommand):
    """A basic implementation of the Abstract Command. The assumption is that the command involves calling a method of the reveiver
    using the user-provided function arguments. Use the optional args to provide the receiver's method runtime arguments.

    Args:
        receiver (object): an object that is actually executing/receiving the command; usually holds the callback function/code
        method (str): the name of the receiver's method to call (it has to be callable and to exist on the receiver)
    """
    def __init__(self, receiver, method: str, *args):
        super().__init__(receiver)
        self._method = method
        self._args = [_ for _ in args]  # this is a list that can be minimally be []

    def append_arg(self, *args):
        self._args.extend([_ for _ in args])

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, args_list):
        self._args = args_list

    def execute(self) -> None:
        return getattr(self._receiver, self._method)(*self._args)


class Command(BaseCommand):
    """A BaseCommand acting as a prototype. The receiver is copied explicitly in a shallow way. The rest are
    assumed to be performance invariant (eg it is not expensive to copy the 'method' attribute, which is a string) and are handled automatically.
    """
    def __copy__(self):
        _ = Command(copy.copy(self._receiver), self._method)
        _.append_arg(*self._args)
        return _


class CommandHistory:
    """The global command history is just a stack; supports 'push' and 'pop' methods."""
    def __init__(self):
        self._history = []

    def push(self, c: Command):
        self._history.append(c)

    def pop(self) -> Command:
        return self._history.pop(0)

    @property
    def stack(self):
        return self._history


class Invoker:
    """A class that simply executes a command and pushes it into its internal command history stack.

    Args:
        history (CommandHistory): the command history object which acts as a stack
    """
    def __init__(self, history: CommandHistory):
        self.history = history

    def execute_command(self, command: Command):
        print("INPUT COMMAND", command)
        if command.execute() is not None:
            self.history.push(command)
