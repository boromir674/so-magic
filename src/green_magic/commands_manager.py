from abc import ABC, abstractmethod
import copy
import attr


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
        print('GGGGGG')
        assert self._args == []
    def append_arg(self, *args):
        self._args.extend([_ for _ in args])

    def execute(self) -> None:
        print(self._receiver, self._method)
        print("ARGS", self._args)
        getattr(self._receiver, self._method)(*self._args)

    def __copy__(self):
        _ = Command(copy.copy(self._receiver), str(self._method))
        _.append_arg(*self._args)
        return _
        # return Command(copy.copy(self._receiver), str(self._method), *self._args)


@attr.s
class CommandsManager:
    datapoints_factory = attr.ib(init=True)

    def __getattr__(self, item):
        return copy.copy(self.prototypes[item])

@attr.s
class ObjectsPool:
    constructor = attr.ib(init=True)
    _objects = attr.ib(init=True, default={})

    def get_object(self, *args, **kwargs):
        key = self._build_hash(*args, **kwargs)
        if key not in ObjectsPool._objects:
            ObjectsPool._objects[key] = self.constructor(*args, **kwargs)
        return ObjectsPool._objects[key]

    def _build_hash(self, *args, **kwargs):
        """Construct a unique string out of the arguments that the constructor receives."""
        return hash('-'.join([str(_) for _ in args]))

    def __getattr__(self, item):
        return ObjectsPool._objects[item]


@attr.s
class CommandHistory:
    """ The global command history is just a stack."""

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
