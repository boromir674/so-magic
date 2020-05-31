import abc
import attr

class EncoderInterface(abc.ABC):
    @abc.abstractmethod
    def encode(self, *args, **kwargs):
        raise NotImplementedError

class AbstractEncoder(EncoderInterface):
    @abc.abstractmethod
    def encode(self, *args, **kwargs):
        raise NotImplementedError


class EncoderFactory:
    @classmethod
    def register_as_subclass(cls, backend_type):
        def wrapper(subclass):
            cls.subclasses[backend_type] = subclass
            return subclass
        return wrapper

    @classmethod
    def create(cls, backend_type, *args, **kwargs):
        if backend_type not in cls.subclasses:
            raise ValueError('Bad "BinnerFactory Backend type" type \'{}\''.format(backend_type))
        return cls.subclasses[backend_type](*args, **kwargs)
    def nominal_encoder(self, *args, **kwargs):
        raise NotImplementedError
