from abc import ABC
import attr

from .features import FeatureInterface


class AbstractFeatureFactory(ABC):

    def get_feature(self, an_id, *args, **kwargs) -> FeatureInterface:
        raise NotImplementedError

    @staticmethod
    def create_from_df(column, an_id, name=None):
        def extractor(dataset):
            return dataset[column]
        if name is None:
            name = an_id
        return TrackingFeat(an_id, name, None, extractor)


class FeatureFactory(AbstractFeatureFactory):

    def get_feature(self, an_id, *args, **kwargs) -> FeatureInterface:
        pass
