from abc import ABC, abstractmethod

from data.features.features import TrackingFeature


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
    def create(cls, backend_type, *args, **kwargs):
        if backend_type not in cls.subclasses:
            raise ValueError('Bad "BinnerFactory Backend type" type \'{}\''.format(backend_type))
        return cls.subclasses[backend_type](*args, **kwargs)

    def get_feature(self, *args, **kwargs) -> TrackingFeature:
        raise NotImplementedError
