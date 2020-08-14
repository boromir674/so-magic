import attr

from data.variables.types import NominalVariableType
from data.features.features import TrackingFeature

@attr.s
class BaseFeatureSet:
    features = attr.ib(init=True, default=[])

    def __len__(self):
        return len(self.features)

    def __getitem__(self, item):
        return self.features[item]

    def __iter__(self):
        return iter(self.features)

    @classmethod
    def from_raw_extractors(cls, data):
        """Create a Feature for each of the lists in the input data (list). Inner lists must satisfy 0 < len(l)"""
        return [TrackingFeature.from_callable(*args) for args in data]


class FeatureSet(BaseFeatureSet):

    @property
    def encoded(self):
        for feature in self.features:
            if str(feature.state) == 'encoded':
                yield feature

    @property
    def not_encoded(self):
        for feature in self.features:
            if str(feature.state) != 'encoded':
                yield feature

    @property
    def binnable(self):
        for feature in self.features:
            if not isinstance(feature.var_type, NominalVariableType):
                yield feature
