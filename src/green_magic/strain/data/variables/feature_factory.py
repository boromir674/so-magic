from abc import ABC, abstractmethod
import attr

from .features import TrackingFeature


class AbstractFeatureFactory(ABC):
    @abstractmethod
    def get_feature(self, *args, **kwargs) -> TrackingFeature:
        raise NotImplementedError


class FeatureFactory(AbstractFeatureFactory):

    @classmethod
    def register_as_subclass(cls, backend_type):
        def wrapper(subclass):
            cls.subclasses[backend_type] = subclass
            return subclass

        return wrapper

    @classmethod
    def create(cls, binner_backend_typeype, *args, **kwargs):
        if binner_backend_typeype not in cls.subclasses:
            raise ValueError('Bad "BinnerFactory Backend type" type \'{}\''.format(binner_backend_typeype))
        return cls.subclasses[binner_backend_typeype](*args, **kwargs)

    def get_feature(self, *args, **kwargs) -> TrackingFeature:
        raise NotImplementedError
