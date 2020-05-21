from abc import ABC, abstractmethod
import attr

from .features import TrackingFeature


class AbstractFeatureFactory(ABC):
    @abstractmethod
    def get_feature(self, *args, **kwargs) -> TrackingFeature:
        raise NotImplementedError


class FeatureFactory(AbstractFeatureFactory):

    def get_feature(self, *args, **kwargs) -> TrackingFeature:
        raise NotImplementedError
