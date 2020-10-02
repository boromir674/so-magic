import attr
import abc


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
