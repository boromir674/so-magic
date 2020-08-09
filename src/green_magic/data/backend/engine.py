import attr
from green_magic.data.dataset import BroadcastingDatapointsFactory
from green_magic.utils import BaseComponent
from green_magic.data.interfaces import TabularRetriever, TabularIterator
from green_magic.data.commands_manager import CommandRegistrator


class EngineType(CommandRegistrator):
    def __new__(mcs, *args, **kwargs):
        x = super().__new__(mcs, *args, **kwargs)
        x._commands = {}
        x.retriever = None
        x.iterator = None
        x.command = mcs.magic_decorator
        return x

    def register_as_subclass(cls, engine_type):
        def wrapper(subclass):
            cls.subclasses[engine_type] = subclass
            return subclass
        return wrapper

    def create(cls, engine_type, *args, **kwargs):
        if engine_type not in cls.subclasses:
            raise ValueError(
                f"Request Engine of type '{engine_type}'; supported are [{', '.join(sorted(cls.subclasses.keys()))}]")
        return cls.subclasses[engine_type](*args, **kwargs)


@attr.s
class DataEngine(BaseComponent, metaclass=EngineType):
    subclasses = {}
    datapoints_factory = BroadcastingDatapointsFactory()

    @classmethod
    def new(cls, engine_name):
        @DataEngine.register_as_subclass(engine_name)
        class RuntimeDataEngine(DataEngine):
            pass
        RuntimeDataEngine.commands_dict = {}

    @classmethod
    def register_as_subclass(cls, engine_type):
        def wrapper(subclass):
            cls.subclasses[engine_type] = subclass
            setattr(cls, engine_type, subclass)
            return subclass
        return wrapper

    @classmethod
    def create(cls, engine_type, *args, **kwargs):
        if engine_type not in cls.subclasses:
            raise ValueError(
                f"Request Engine of type '{engine_type}'; supported are [{', '.join(sorted(cls.subclasses.keys()))}]")
        return cls.subclasses[engine_type](*args, **kwargs)

    @classmethod
    def observations(cls, data_structure='tabular-data'):
        def wrapper(function):
            if hasattr(function, '__code__'):  # it a function (def func_name ..)
                print(f"Observation decor in Engine: {function.__code__.co_name}")
                def observations(file_path, **kwargs):
                    res = function(file_path, **kwargs)
                    datapoints = cls.datapoints_factory.create(data_structure, res, [_ for _ in cls.iterator.columnnames], cls.retriever, cls.iterator)
                cls.registry[function.__code__.co_name] = cls.command_factory(observations)
                cls._commands[function.__code__.co_name] = cls.command_factory(observations)
            else:
                raise RuntimeError("Expected a function to be decorated.")
            return function
        return wrapper
