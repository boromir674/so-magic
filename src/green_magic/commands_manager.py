from abc import ABC, abstractmethod
import copy
import attr


class CommandInterace(ABC):

    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError


class BaseCommand(CommandInterace, ABC):
    def __init__(self, receiver, *args):
        self._receiver = receiver


class Command(BaseCommand):
    def __init__(self, receiver, method, *args):
        super().__init__(receiver, *args)
        self._method = method
        self._args = list(args)  # this is tuple that can be minimally be ()

    def append_arg(self, element):
        self._args.append(element)

    def execute(self) -> None:
        return getattr(self._receiver, self._method)(*self._args)

    def __copy__(self):
        return Command(copy.copy(self._receiver), self._method, copy.copy(self._args))


@attr.s
class CommandsManager:
    prototypes = attr.ib(init=True, default={
        'empty': Command(None, 'Null'),
    })

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

    def __getattribute__(self, item):
        return ObjectsPool._objects[item]
