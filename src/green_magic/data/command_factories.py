from abc import ABC, abstractmethod
import attr
from green_magic.utils import Command
from green_magic.utils import Subject


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
                ffunc = a[0]
                mcs._wrapper(ffunc, *a[1:], **ka)
                return ffunc
            print("DEBUG magic_decorator 4, func: {}".format(str(func)))
            return wrapper

        if callable(arg):
            print("Decoration invokation WITHOUT parenthesis")
            _ = decorator(arg)
            print("OUT: {}".format(str(_)))
            print(type(_))
            return _  # return 'wrapper'
        else:
            print("Decoration invokation WITH parenthesis")
            _ = decorator
            print(f"OUT: {str(_)}")
            print(type(_))
            return _  # ... or 'decorator'

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

    def func_decorator(cls):
        def wrapper(a_callable):
            if hasattr(a_callable, '__code__'):  # it a function (def func_name ..)
                print(f"Registering input function {a_callable.__code__.co_name}")
                cls.registry[a_callable.__code__.co_name] = a_callable
            else:
                raise RuntimeError(f"Expected a function to be decorated; got {type(a_callable)}")
            return a_callable
        return wrapper

class AbstractCommandFactory(ABC):
    @abstractmethod
    def construct(self, *args, **kwargs) -> Command:
        raise NotImplementedError

class BaseCommandFactory(AbstractCommandFactory, ABC):

    subclasses = {}

    @classmethod
    def register_as_subclass(cls, factory_type):
        def wrapper(subclass):
            cls.subclasses[factory_type] = subclass
            return subclass
        return wrapper

    @classmethod
    def create(cls, factory_type, *args, **kwargs):
        if factory_type not in cls.subclasses:
            raise ValueError('Bad "Factory type" \'{}\''.format(factory_type))
        return cls.subclasses[factory_type](*args, **kwargs)


@BaseCommandFactory.register_as_subclass('generic')
class GenericCommandFactory(AbstractCommandFactory):
    def construct(self, *args, **kwargs) -> Command:
        return Command(*args, **kwargs)

@BaseCommandFactory.register_as_subclass('function')
class FunctionCommandFactory(AbstractCommandFactory):
    def construct(self, *args, **kwargs) -> Command:
        if len(args) < 1:
            raise RuntimeError("Will break")
        return Command(args[0], '__call__', *args[1:])


@BaseCommandFactory.register_as_subclass('encode_nominal_subsets')
class NominalAttributeListEncodeCommandFactory(AbstractCommandFactory):
    def construct(self, *args, **kwargs) -> Command:
        from green_magic.data.features.phis import ListOfCategoricalPhi, DatapointsAttributePhi
        assert len(args) > 0
        datapoints = args[0]
        attribute = args[1]
        new_attribute = args[2]
        def _command(_datapoints, _attribute, _new_attribute):
            phi = ListOfCategoricalPhi(DatapointsAttributePhi(_datapoints))
            new_values = phi(_attribute)
            _datapoints.mutator.add_column(_datapoints, new_values, _new_attribute)
        return Command(_command, '__call__', datapoints, attribute, new_attribute)


class CommandFactory:
    """A factory class able to construct new command objects."""
    constructors = {k: v().construct for k, v in BaseCommandFactory.subclasses.items()}
    @classmethod
    def pick(cls, *args, **kwargs):
        decision = {True: 'function', False: 'generic'}
        is_function = hasattr(args[0], '__code__')
        print(f'is function?: {is_function}')
        print(f'PICK: {args}')
        dec2 = {'function': lambda x: x[0].__code__.co_name, 'generic': lambda x: type(x[0]).__name__ + '-' + x[1]}
        return decision[is_function], kwargs.get('name', dec2[decision[is_function]](args))

    @classmethod
    def create(cls, *args, **kwargs) -> Command:
        """Call to create a new Command object. The input arguments can be in two formats:

        1. create(an_object, method, *arguments)
        In this case the command is of the form an_object.method(*arguments)

        2. create(a_function, *arguments)
        In this case the command is of the form a_function(*arguments)

        Returns:
            Command: an instance of a command object
        """
        print("CMD FCT")
        print("args: ", args)
        print("kwargs", kwargs)

        key, name = cls.pick(*args, **kwargs)
        print(f"KEY: {key}, NAME: {name}")
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
        assert args
        self._state, self.name = self.command_factory.create(*args, **kwargs)
        self.notify()
        return self._state
