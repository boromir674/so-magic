from typing import Tuple
import attr

from so_magic.utils import Subject, Command, CommandFactoryInterface, CommandFactoryType


class BaseCommandFactory(metaclass=CommandFactoryType):
    pass


@BaseCommandFactory.register_as_subclass('generic')
class GenericCommandFactory(CommandFactoryInterface):
    """Command Factory that constructs a command given all the necessary arguments.

    Assumes the 1st argument is the 'receiver' (see Command module),
    2nd is the method to call on the receiver and the rest are the method's runtime arguments.
    """
    def construct(self, *args, **kwargs) -> Command:
        """Construct a command object (Command class instance).

        Assumes the 1st argument is the 'receiver' (see Command module),
        2nd is the method to call on the receiver and the rest are the method's runtime arguments.

        Returns:
            Command: the command object
        """
        return Command(*args, **kwargs)


@BaseCommandFactory.register_as_subclass('function')
class FunctionCommandFactory(CommandFactoryInterface):
    """Command Factory that constructs a command assuming the 1st argument is a python function.

    Assumes that the function (1st argument) acts as the the 'receiver' (see Command module),
    2nd is the method to call on the receiver and the rest are the method's runtime arguments.
    """
    def construct(self, *args, **kwargs) -> Command:
        """Construct a command object (Command class instance).

        Assumes that the 1st argument is a python function and that it acts as the the 'receiver' (see Command module).
        The rest are the function's runtime arguments.

        Raises:
            RuntimeError: [description]

        Returns:
            Command: [description]
        """
        if len(args) < 1:
            raise RuntimeError("Will break")
        return Command(args[0], '__call__', *args[1:])


class CommandFactory:
    """A factory class able to construct new command objects."""
    constructors = {k: v().construct for k, v in BaseCommandFactory.subclasses.items()}

    @classmethod
    def pick(cls, *args, **kwargs):
        decision = {True: 'function', False: 'generic'}
        is_function = hasattr(args[0], '__code__')
        dec2 = {'function': lambda x: x[0].__code__.co_name, 'generic': lambda x: type(x[0]).__name__ + '-' + x[1]}
        return decision[is_function], kwargs.get('name', dec2[decision[is_function]](args))

    @classmethod
    def create(cls, *args, **kwargs) -> Tuple[Command, str]:

        key, name = cls.pick(*args, **kwargs)
        if len(args) < 1:
            raise RuntimeError(args)
        return cls.constructors[key](*args), name


@attr.s
class MagicCommandFactory(Subject):
    """Instances of this class act as callable command factories that notify,
    subscribed observers/listeners upon new command object creation.

    Args:
        command_factory (CommandFactory, optional): an instance of a CommandFActory
    """
    command_factory = attr.ib(init=True, default=CommandFactory())

    def __call__(self, *args, **kwargs):
        self.state, self.name = self.command_factory.create(*args, **kwargs)
        self.notify()
        return self.state
