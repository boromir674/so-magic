import copy
from abc import ABC
from .command_interface import CommandInterface

__all__ = ['Command', 'Invoker', 'CommandHistory', 'CommandInterface']


# class CommandInterface(ABC):
#     """Standalone command, encapsulating all logic and data needed, required for execution."""
#     @abstractmethod
#     def execute(self) -> None:
#         """Execute the command; run the commands logic."""
#         raise NotImplementedError


class AbstractCommand(CommandInterface, ABC):
    """An abstract implementation of the CommandInterface.

    The assumption is that the command involves a main 'receiver' object.
    Commands of this type follow the receiver.method(*args) pattern/model.
    The receiver object usually is commonly acting as an 'oracle' on the
    application or on the situation/context.

    Args:
        receiver (object): usually holds the callback function/code with the business logic
    """
    def __init__(self, receiver):
        self._receiver = receiver


class BaseCommand(AbstractCommand):
    """A concrete implementation of the Abstract Command.

    This command simply invokes a 'method' on the 'receiver'. When constructing
    instances of BaseCommand make sure you respect the 'method' signature. For
    that, you can use the *args to provide the receiver's method arguments.

    Intuitively, what happens is

    .. code-block:: python

        receiver.method(*args)

    and that is another way to show how the *args are passed to method

    Args:
        receiver (object): an object that is actually executing/receiving the command; usually holds the callback
        function/code
        method (str): the name of the receiver's method to call (it has to be callable and to exist on the receiver)
    """
    def __init__(self, receiver, method: str, *args):
        super().__init__(receiver)
        self._method = method
        self._args = list(args)  # this is a list that can be minimally be []

    def append_arg(self, *args):
        self._args.extend(args)

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, args_list):
        self._args = list(args_list)

    def execute(self) -> None:
        return getattr(self._receiver, self._method)(*self._args)


class Command(BaseCommand):
    """An runnable/executable Command that acts as a prototype through the 'copy' python magic function.

    When a command instance is invoked with 'copy', the receiver is copied explicitly in a shallow way. The rest of the
    command arguments are assumed to be performance invariant (eg it is not expensive to copy the 'method' attribute,
    which is a string) and are handled automatically.
    """
    def __copy__(self):
        _ = Command(copy.copy(self._receiver), self._method)
        _.append_arg(*self._args)
        return _


class CommandHistory:
    """The global command history is just a stack; supports 'push' and 'pop' methods."""
    def __init__(self):
        self._history = []

    def push(self, command: Command):
        self._history.append(command)

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
