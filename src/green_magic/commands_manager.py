from abc import ABC, abstractmethod
import copy
import attr
from green_magic.utils import Observer, Subject


class CommandInterface(ABC):

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError

@attr.s
class AbstractCommand(CommandInterface, ABC):
    _receiver = attr.ib(init=True)


class Command(AbstractCommand):
    def __init__(self, receiver, method, *args):
        super().__init__(receiver)
        self._method = method
        self._args = [_ for _ in args]  # this is a list that can be minimally be []

    def append_arg(self, *args):
        self._args.extend([_ for _ in args])

    def execute(self) -> None:
        getattr(self._receiver, self._method)(*self._args)

    def __copy__(self):
        _ = Command(copy.copy(self._receiver), str(self._method))
        _.append_arg(*self._args)
        return _
        # return Command(copy.copy(self._receiver), str(self._method), *self._args)


@attr.s
class CommandsManager(Observer):
    datapoints_factory = attr.ib(init=True)
    prototypes = attr.ib(init=True, default={})

    def update(self, subject: Subject) -> None:
        # if subject._state
        # self.prototypes
        pass

    def __getattr__(self, item):
        if item not in self.prototypes:
            raise KeyError(f"Item '{item}' not found in [{', '.join(str(_) for _ in self.prototypes.keys())}]")
        return self.prototypes[item]


@attr.s
class ObjectsPool:
    """A generic object pool able to return a reference to an object upon request. Whenever an object is requested a
    hash is built out of the (request) arguments, which is then checked against the registry of keys to determine
    whether the object is present in the pool or to create (using the local constructor attribute) and insert a new one
     (in the pool)."""
    constructor = attr.ib(init=True)
    _objects = attr.ib(init=True, default={})

    def get_object(self, *args, **kwargs):
        key = self._build_hash(*args, **kwargs)
        if key not in self._objects:
            self._objects[key] = self.constructor(*args, **kwargs)
        return self._objects[key]

    def _build_hash(self, *args, **kwargs):
        """Construct a unique string out of the arguments that the constructor receives."""
        return hash('-'.join([str(_) for _ in args]))

    def __getattr__(self, item):
        return self._objects[item]


@attr.s
class CommandHistory:
    """The global command history is just a stack; supports 'push' and 'pop' methods."""

    _history = attr.ib(init=False, default=[])
    @_history.validator
    def validate_history(self, attribute, value):
        if type(value) != list:
            raise ValueError(f"Expected a list, instead a {type(value).__name__} was given")

    def push(self, c: Command):
        self._history.append(c)

    def pop(self) -> Command:
        return self._history.pop(0)


@attr.s
class Invoker:
    history = attr.ib(init=False, default=CommandHistory())

    def execute_command(self, command: Command):
        if command.execute():
            self.history.push(command)
