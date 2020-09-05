from green_magic.data.command_factories import MagicCommandFactory, CommandRegistrator


class EngineType(CommandRegistrator):

    def __new__(mcs, *args, **kwargs):
        x = super().__new__(mcs, *args, **kwargs)
        x._commands = {}
        x.retriever = None
        x.iterator = None
        x.mutator = None
        x.backend = None
        x.command = mcs.magic_decorator
        x.command_factory = MagicCommandFactory()
        return x

    def dec(cls, data_structure='tabular-data'):
        def wrapper(a_callable):
            if hasattr(a_callable, '__code__'):  # it a function (def func_name ..)
                name = a_callable.__code__.co_name
                if name == 'observations':
                    def observations(file_path, **kwargs):
                        _observations = a_callable(file_path, **kwargs)
                        datapoints = cls.backend.datapoints_factory.create(data_structure, _observations, [_ for _ in []],
                                                                   cls.retriever(),
                                                                   cls.iterator(),
                                                                   cls.mutator(),
                                                                   file_path=file_path)
                    cls.registry[name] = observations
                    cls._commands[name] = cls.command_factory(observations)
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
                def observations(file_path, **kwargs):
                    res = function(file_path, **kwargs)
                    datapoints = cls.datapoints_factory.create(data_structure, res, [_ for _ in cls.iterator.columnnames], cls.retriever, cls.iterator)
                cls.registry[function.__code__.co_name] = cls.command_factory(observations)
                cls._commands[function.__code__.co_name] = cls.command_factory(observations)
            else:
                raise RuntimeError("Expected a function to be decorated.")
            return function
        return wrapper
