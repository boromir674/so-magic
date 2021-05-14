from typing import Callable
import attr
from so_magic.utils import Command, Subject, CommandFactoryInterface, CommandFactoryType


class DataManagerCommandFactoryBuilder(metaclass=CommandFactoryType):
    @classmethod
    def create_factory(cls, name, callback):
        @DataManagerCommandFactoryBuilder.register_as_subclass(name)
        class DataManagerRuntimeCommandFactory(CommandFactoryInterface):
            def construct(self, *args, **kwargs) -> Command:
                receiver = args[0]
                def command(*runtime_args):
                    callback(receiver, *runtime_args)
                return Command(command, '__call__', *args[1:])


@attr.s
class DataManagerCommandFactory(Subject):
    _data_manager = attr.ib(init=True)
    command_factory = attr.ib(init=True, default=DataManagerCommandFactoryBuilder)

    def __call__(self, command_type, *args, **kwargs):
        self.state = self.command_factory.create(command_type).construct(self._data_manager, *args, **kwargs)
        self.name = command_type
        self.notify()
        return self.state

    def build_command_prototype(self):
        def wrapper(a_callable: Callable) -> Callable:
            """Build and register a new Command given a callable object that holds the important business logic.

            Args:
                a_callable (Callable): the Command's important underlying business logic
            """
            if hasattr(a_callable, '__code__'):  # a_callable object has been defined with the def python keyword
                decorated_function_name = a_callable.__code__.co_name
                self.command_factory.create_factory(decorated_function_name, a_callable)
                self(decorated_function_name)
            else:
                raise RuntimeError(f"Expected a function to be decorated; got {type(a_callable)}")
            return a_callable
        return wrapper
