import inspect
import attr
from green_magic.utils import Command
from green_magic.utils import Subject, Observer


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


class MyDecorator(type):
    """Metaclass that provides a decorator able to be invoked both with and without parenthesis.
    The wrapper function logic should be implemented by the client code.
    """
    @classmethod
    def magic_decorator(mcs, arg=None):
        def decorator(func):
            def wrapper(*a, **ka):
                mcs._wrapper(func, *a, **ka)
                return func(*a, **ka)
            return wrapper

        if callable(arg):
            return decorator(arg)  # return 'wrapper'
        else:
            return decorator  # ... or 'decorator'

    def _wrapper(cls, function, *args, **kwargs):
        pass

class EngineCommandRegistrator(MyDecorator):
    """Engines inheriting from this class

    Args:
        MyDecorator ([type]): [description]

    Raises:
        RuntimeError: [description]
        RuntimeError: [description]
    """
    def __new__(mcs, *args, **kwargs):
        class_object = super().__new__(mcs, *args, **kwargs)
        class_object.state = None
        return class_object

    command_factory = MagicCommandFactory()

    @classmethod
    def _wrapper(cls, function, *args, **kwargs):
        a_callable = function
        if hasattr(a_callable, '__code__'):  # it a function (def func_name ..)
            cls.state = (kwargs.get('name', kwargs.get('key', a_callable.__code__.co_name)), cls.command_factory(function))
        else:
            if not hasattr(a_callable, '__call__'):
                raise RuntimeError(
                    f"Expected an class definition with a '__call__' instance method defined 1. Got {type(a_callable)}")
            members = inspect.getmembers(a_callable)
            if not ('__call__', a_callable.__call__) in members:
                raise RuntimeError(
                    f"Expected an class definition with a '__call__' instance method defined 2. Got {type(a_callable)}")
            instance = a_callable()
            cls.state = (kwargs.get('name', kwargs.get('key', getattr(instance, 'name', type(a_callable).__name__))), cls.command_factory(instance))


class CommandRegistrator(MyDecorator):
    command_factory = MagicCommandFactory()
    state = None

    def _wrapper(cls, function, *args, **kwargs):
        a_callable = function
        if hasattr(a_callable, '__code__'):  # it a function (def func_name ..)
            cls.state = (kwargs.get('name', kwargs.get('key', a_callable.__code__.co_name)), cls.command_factory(function))
        else:
            if not hasattr(a_callable, '__call__'):
                raise RuntimeError(
                    f"Expected an class definition with a '__call__' instance method defined 1. Got {type(a_callable)}")
            members = inspect.getmembers(a_callable)
            if not ('__call__', a_callable.__call__) in members:
                raise RuntimeError(
                    f"Expected an class definition with a '__call__' instance method defined 2. Got {type(a_callable)}")
            instance = a_callable()
            cls.state = (kwargs.get('name', kwargs.get('key', getattr(instance, 'name', type(a_callable).__name__))), cls.command_factory(instance))
        return a_callable


@attr.s
class CommandsAccumulator(Observer):
    commads = attr.ib(init=False, default={})

    def update(self, subject: Subject) -> None:
        self.commads[subject.name] = subject.state


@attr.s
class CommandsManager:
    """[summary]

    Args:
        prototypes (dict, optional): initial prototypes to be supplied
        command_factory (callable, optional): a callable that returns an instance of Command
    """
    _commands_accumulator = attr.ib(init=True, default=CommandsAccumulator())

    @property
    def prototypes(self):
        return self._commands_accumulator.commads

    def __getattr__(self, item):
        if item not in self._commands_accumulator.commads:
            raise KeyError(f"Item '{item}' not found in [{', '.join(str(_) for _ in self._commands_accumulator.commads.keys())}]")
        return self._commands_accumulator.commads[item]
