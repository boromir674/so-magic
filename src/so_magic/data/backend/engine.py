"""This module defines a way to create Data Engines and to register new commands that a Data Engine can execute.
"""
from collections import defaultdict
from typing import Tuple, Callable
from .engine_command_factory import MagicCommandFactory


class MyDecorator(type):
    """Metaclass that provides a decorator able to be invoked both with and without parenthesis.
    The wrapper function logic should be implemented by the client code.
    """
    @classmethod
    def magic_decorator(mcs, arg=None):
        def decorator(_func):
            def wrapper(*a, **ka):
                ffunc = a[0]
                mcs._wrapper(ffunc, *a[1:], **ka)
                return ffunc
            return wrapper

        if callable(arg):
            _ = decorator(arg)
            return _  # return 'wrapper'
        _ = decorator
        return _  # ... or 'decorator'


class CommandRegistrator(MyDecorator):
    """Classes can use this class as metaclass to obtain a single registration point accessible as class attribute.
    """
    def __new__(mcs, *args, **kwargs):
        class_object = super().__new__(mcs, *args, **kwargs)
        class_object.state = None
        class_object.registry = {}
        return class_object

    def __getitem__(cls, item):
        if item not in cls.registry:
            raise RuntimeError(f"Key '{item}' fot found in registry: "
                               f"[{', '.join(str(x) for x in cls.registry.keys())}]")
        return cls.registry[item]

    # Legacy feature, not currently used in production
    def func_decorator(cls):
        def wrapper(a_callable):
            if hasattr(a_callable, '__code__'):  # it a function (def func_name ..)
                cls.registry[a_callable.__code__.co_name] = a_callable
            else:
                raise RuntimeError(f"Expected a function to be decorated; got {type(a_callable)}")
            return a_callable
        return wrapper


class EngineType(CommandRegistrator):
    """Tabular Data Backend type representation.

    Classes using this class as metaclass gain certain class attributes such as
    attributes related to tabular data operations (retriever, iterator, mutator) and attributes related to constructing
    command object prototypes (command_factory attribute).
    """

    def __new__(mcs, *args, **kwargs):
        engine_type = super().__new__(mcs, *args, **kwargs)
        engine_type._commands = {}
        engine_type.retriever = None
        engine_type.iterator = None
        engine_type.mutator = None
        engine_type.backend = None
        engine_type.command = mcs.magic_decorator
        engine_type.command_factory = MagicCommandFactory()
        engine_type._receivers = defaultdict(lambda: engine_type._generic_cmd_receiver,
                                             observations=engine_type._observations_from_file_cmd_receiver)
        return engine_type

    def _observations_from_file_cmd_receiver(cls, callable_function, **kwargs) -> Tuple[callable, dict]:
        """Create the Receiver of a command that creates datapoints from a file.

        It also creates the kwargs that a Command factory method would need along with the receiver object.

        It is assumed that the business logic is executed in the callable function supplied.
        You can use the data_structure "keyword" argument (kwarg) to indicate how should we parse/read
        the raw data from the file. Supported values: 'tabular-data'

        Args:
            callable_function (callable): the business logic that shall run in the command

        Returns:
            Union[callable, dict]: the receiver object that can be used to create a Command instance
                                    and parameters to pass in the kwargs of the command factory method (eg
                                    cls.command_factory(a_function, **kwargs_dict))
        """

        def observations(file_path, **runtime_kwargs):
            """Construct the observations attribute of a Datapoints instance.

            The signature of this function determines the signature that is used at runtime
            when the command will be executed. Thus the command's arguments at runtime
            should follow the signature of this function.

            Args:
                file_path (str): the file in disk that contains the data to be read into observations
            """
            # create the observations object
            _observations = callable_function(file_path, **runtime_kwargs)
            # create the datapoints object and let the datapoints factory notify its listeners (eg a datapoints manager)
            _ = cls.backend.datapoints_factory.create(kwargs.get('data_structure', 'tabular-data'),
                                                      _observations, [],
                                                      cls.retriever(),
                                                      cls.iterator(),
                                                      cls.mutator(),
                                                      file_path=file_path)

        return observations, {}

    def _generic_cmd_receiver(cls, callable_function, **kwargs) -> Tuple[callable, dict]:
        """Create the Receiver of a generic command.

        It also creates the kwargs that a Command factory method would need along with the receiver object.

        It is assumed that the business logic is executed in the callable function.

        Args:
            callable_function (Callable): the business logic that shall run in the command

        Returns:
            Union[callable, dict]: the receiver object that can be used to create a Command instance
                                    and parameters to pass in the kwargs of the command factory
                                    (eg cls.command_factory(a_function, **kwargs_dict))
        """

        def a_function(*args, **runtime_kwargs):
            """Just execute the business logic that is provided at runtime.

            The signature of this function determines the signature that is used at runtime
            when the command will be executed. Thus the command's arguments at runtime
            should follow the signature of this function. So, the runtime function
            can have any signature (since a_function uses flexible *args and **runtime_kwargs).
            """
            callable_function(*args, **runtime_kwargs)

        return a_function, {'name': lambda name: name}

    def _build_command(cls, a_callable: callable, registered_name: str, data_structure='tabular-data'):
        """Build a command given a callable object with the business logic and register the command under a name.

        Creates the required command Receiver and arguments, given a function at runtime. If the function is named
        'observations' then the Receiver is tailored to facilitate creating a Datapoints instance given a file path
        with the raw data.

        Args:
            a_callable (Callable): holds the business logic that executes when the command shall be executed
            registered_name (str): the name under which to register the command (can be used to reference the command)
            data_structure (str, optional): useful when creating a command that instantiates Datapoints objects.
            Defaults to 'tabular-data'.
        """
        receiver, kwargs_data = cls._receivers[registered_name](a_callable, data_structure=data_structure)
        cls.registry[registered_name] = receiver
        cls._commands[registered_name] = cls.command_factory(receiver, **{k: v for k, v in dict(kwargs_data, **{
            'name': kwargs_data.get('name', lambda name: '')(registered_name)}).items() if v})

    def dec(cls, data_structure='tabular-data') -> Callable[[Callable], Callable]:
        """Register a new command that executes the business logic supplied at runtime.

        Decorate a function so that its body acts as the business logic that runs as part of a Command.
        The name of the function can be used to later reference the Command (or a prototype object of the Command).

        Using the 'observations' name for your function will register a command that upon execution creates a new
        instance of Datapoints (see Datapoints class), provided that the runtime function returns an object that acts as
        the 'observations' attribute of a Datapoints object.

        Args:
            data_structure (str, optional): useful when the function name is 'observations'. Defaults to 'tabular-data'.
        """

        def wrapper(a_callable: Callable) -> Callable:
            """Build and register a new Command given a callable object that holds the important business logic.

            Args:
                a_callable (Callable): the Command's important underlying business logic
            """
            if hasattr(a_callable, '__code__'):  # a_callable object has been defined with the def python keyword
                decorated_function_name = a_callable.__code__.co_name
                cls._build_command(a_callable, decorated_function_name, data_structure=data_structure)
            else:
                raise RuntimeError(f"Expected a function to be decorated; got {type(a_callable)}")
            return a_callable

        return wrapper


class DataEngine(metaclass=EngineType):
    """Facility to create Data Engines."""
    subclasses = {}

    @classmethod
    def new(cls, engine_name: str) -> EngineType:
        """Create a Data Engine object and register it under the given name, to be able to reference it by name.

        Creates a Data Engine that serves as an empty canvas to add attributes and Commands.

        Args:
            engine_name (str): the name under which to register the Data Engine

        Returns:
            EngineType: the Data Engine object
        """

        @DataEngine.register_as_subclass(engine_name)
        class RuntimeDataEngine(DataEngine):
            pass

        return RuntimeDataEngine

    @classmethod
    def register_as_subclass(cls, engine_type: str):
        """Indicate that a class is a subclass of DataEngine and register it under the given name.

        It also sets the engine_type attribute on the decorate class to be equal to the subclass.

        Args:
            engine_type (str): the name under which to register the Data Engine
        """

        def wrapper(subclass) -> type:
            cls.subclasses[engine_type] = subclass
            setattr(cls, engine_type, subclass)
            return subclass

        return wrapper
