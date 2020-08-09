import inspect
import attr
from green_magic.utils import Command
from green_magic.utils import Subject, Observer


class MyDecorator(type):
    """Metaclass that provides a decorator able to be invoked both with and without parenthesis.
    The wrapper function logic should be implemented by the client code.
    """
    @classmethod
    def magic_decorator(mcs, arg=None):
        print("DEBUG magic_decorator 1, args:", str(arg))
        def decorator(func):
            print("DEBUG magic_decorator 2, args:", str(func))
            def wrapper(*a, **ka):
                print("DEBUG magic_decorator 3, args: [{}]".format(', '.join(str(x) for x in a)))
                mcs._wrapper(func, *a, **ka)
                return func(*a, **ka)
            return wrapper

        if callable(arg):
            return decorator(arg)  # return 'wrapper'
        else:
            return decorator  # ... or 'decorator'

    def _wrapper(cls, function, *args, **kwargs):
        print('LA8OS')
        raise NotImplementedError


class CommandRegistrator(MyDecorator):
    """Classes can use this class as metaclass to obtain a single registration point accessible as class attribute
    """
    def __new__(mcs, *args, **kwargs):
        class_object = super().__new__(mcs, *args, **kwargs)
        class_object.state = None
        class_object.registry = {}
        return class_object

    def __getitem__(self, item):
        if item not in self.registry:
            raise RuntimeError(f"Key '{item}' fot found in registry: [{', '.join(str(x) for x in self.registry.keys())}]")
        return self.registry[item]

@attr.s
class CommandFactory(Subject):
    """A factory class able to construct new command objects."""
    command_constructor = attr.ib(init=True, default=Command)

    def create(self, *args) -> Command:
        """Call to create a new Command object. The input arguments can be in two formats:

        1. create(an_object, method, *arguments)
        In this case the command is of the form an_object.method(*arguments)

        2. create(a_function, *arguments)
        In this case the command is of the form a_function(*arguments)

        Returns:
            Command: an instance of a command object
        """
        is_function = hasattr(args[0], '__code__')
        if is_function:  # if receiver is a function; creating from function
            return self.command_constructor(args[0], '__call__', *args[1:])
        return self.command_constructor(args[0], args[1], *args[2:])

@attr.s
class MagicCommandFactory(Subject):
    """Instances of this class act as callable command factories that notify,
    subscribed observers/listeners upon new command object creation.

    Args:
        command_factory (CommandFactory, optional): an instance of a CommandFActory
    """
    command_factory = attr.ib(init=True, default=CommandFactory())

    def __call__(self, *args, **kwargs):
        self._state = self.command_factory.create(*args)
        self.notify()
        return self._state


@attr.s
class CommandsAccumulator(Observer):
    """"""
    commands = attr.ib(init=False, default={})

    def update(self, subject: Subject) -> None:
        self.commands[getattr(subject, 'name', str(subject.state))] = subject.state

@attr.s
class CommandGetter:
    _commands_accumulator = attr.ib(init=True, default=CommandsAccumulator())

    def __getattr__(self, item):
        if item not in self._commands_accumulator.commands:
            raise KeyError(f"Item '{item}' not found in [{', '.join(str(_) for _ in self._commands_accumulator.commands.keys())}]")
        return self._commands_accumulator.commands[item]


@attr.s
class CommandsManager:
    """[summary]

    Args:
        prototypes (dict, optional): initial prototypes to be supplied
        command_factory (callable, optional): a callable that returns an instance of Command
    """
    _commands_getter = attr.ib(init=True, default=CommandGetter())

    @property
    def command(self):
        return self._commands_getter

    @property
    def commands_dict(self):
        return self._commands_accumulator.commands

    def __getattr__(self, item):
        if item not in self._commands_accumulator.commands:
            raise KeyError(f"Item '{item}' not found in [{', '.join(str(_) for _ in self._commands_accumulator.commands.keys())}]")
        return self._commands_accumulator.commands[item]
