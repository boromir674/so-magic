from green_magic.data.dataset import BroadcastingDatapointsFactory
from green_magic.data.command_factories import MagicCommandFactory, CommandRegistrator


class EngineType(CommandRegistrator):
    datapoints_factory = BroadcastingDatapointsFactory()

    def __new__(mcs, *args, **kwargs):
        x = super().__new__(mcs, *args, **kwargs)
        x._commands = {}
        x.retriever = None
        x.iterator = None
        x.mutator = None
        x.command = mcs.magic_decorator
        x.command_factory = MagicCommandFactory()
        return x

    def dec(cls, data_structure='tabular-data'):
        def wrapper(a_callable):
            if hasattr(a_callable, '__code__'):  # it a function (def func_name ..)
                name = a_callable.__code__.co_name
                print(f"ADW function {name}")
                obs_funct = a_callable
                print("DEBUG NAME:", name)
                if name == 'observations':
                    def observations(file_path, **kwargs):
                        print(f"FP: {file_path}")
                        print(f"Callable: {a_callable.__code__.co_name}, {a_callable}")
                        print(f"Kwargs: {kwargs}")
                        _observations = a_callable(file_path, **kwargs)
                        datapoints = cls.datapoints_factory.create(data_structure, _observations, [_ for _ in []],
                                                                   cls.retriever(),
                                                                   cls.iterator(),
                                                                   cls.mutator())
                        # datapoints._attributes = [_ for _ in cls.iterator.columnnames(datapoints)]

                    cls.registry[name] = observations
                    cls._commands[name] = cls.command_factory(observations)
                    # obs_funct = lambda json_path: _observations(json_path)
                elif name == 'add_attribute':
                    def add_attribute(*args, **kwargs):
                        a_callable(*args, **kwargs)
                    cls.registry[name] = add_attribute
                    cls._commands[name] = cls.command_factory(add_attribute)
                else:
                    def a_function(*args, **kwargs):
                        a_callable(*args, **kwargs)
                    cls.registry[name] = a_function
                    cls._commands[name] = cls.command_factory(a_function, name=name)
            else:
                raise RuntimeError(f"Expected a function to be decorated; got {type(a_callable)}")
            return a_callable
        return wrapper

class DataEngine(metaclass=EngineType):
    subclasses = {}

    @classmethod
    def new(cls, engine_name):
        @DataEngine.register_as_subclass(engine_name)
        class RuntimeDataEngine(DataEngine):
            pass
        return RuntimeDataEngine

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
