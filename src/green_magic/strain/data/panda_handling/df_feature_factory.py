import attr
from ..variables import TrackingFeature, FeatureFactory


@attr.s
class AbstractDfFeature:
    feat = attr.ib(init=True)

    @property
    def nb_unique(self):
        return self._df[self._column].nunique()

    def update(self, *args, **kwargs):
        if 2 < len(args):
            self._column = args[2]
        super().update(*args, **kwargs)


@attr.s
class DFFeature(AbstractDfFeature):
    # _df = attr.ib(init=True, default=None)
    _column = attr.ib(init=True, default='')

    def unique(self):
        return list(self._df[self.id].unique())


class DFFeatureFactory(FeatureFactory):
    @classmethod
    def get_feature(cls, an_id, *args, **kwargs):
        handler = args[1]
        # df = dataset.handler.data
        def function(x_dataset):
            return handler.extract(an_id)
        _ = DFFeature(TrackingFeature.from_extractor(an_id, function), kwargs.get('name', an_id), function)
        _.df = df
        _._column = an_id
        return _

    @classmethod
    def from_list(cls, a_list, **kwargs):
        return [cls.get_feature(x, kwargs['dataset']) for x in a_list]


df_features_factory = DFFeatureFactory()

from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3