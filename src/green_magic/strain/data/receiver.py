import attr


@attr.s
class Manager2:
    def normalize(self, *args, **kwargs):
        raise NotImplementedError

    def discretize(self, *args, **kwargs):
        raise NotImplementedError

    def encode(self, *args, **kwargs):
        raise NotImplementedError

    def do_something(self, a: str) -> None:
        print(f"\nReceiver: Working on ({a}.)", end="")

    def do_something_else(self, b: str) -> None:
        print(f"\nReceiver: Also working on ({b}.)", end="")

import attr

@attr.s
class BaseReceiver(AbstractReceiver):
    data_handler = attr.ib(init=True, default=None)

    def normalize(self, *args, **kwargs):
        return args[1].extractor(args[0])
    def discretize(self, *args, **kwargs):
        pass
    def encode(self, *args, **kwargs):
        pass


class ReceiverFactory:

    @classmethod
    def get_receiver(cls) -> BaseReceiver:
        pass


import abc
@attr.s
class Manager:
    backend = attr.ib(init=True)


class Backend(abc.ABC):
    subclasses = {}

    @classmethod
    def register_as_subclass(cls, backend_type):
        def wrapper(subclass):
            cls.subclasses[backend_type] = subclass
            return subclass

        return wrapper

    @classmethod
    def create(cls, backend_type, *args, **kwargs):
        if backend_type not in cls.subclasses:
            raise ValueError('Bad "Data Backend type" type \'{}\''.format(backend_type))
        return cls.subclasses[backend_type](*args, **kwargs)

    @property
    @abc.abstractmethod
    def features_factory(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def commands_manager(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def computing(self):
        raise NotImplementedError
