from collections import OrderedDict
import attr

from so_magic.utils import Observer, Subject
from so_magic.data.variables.types import NominalVariableType
from so_magic.data.features.features import TrackingFeature


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


@attr.s
class FeatureConfiguration(Observer):
    _variables = attr.ib(init=True)
    _feature_vectors = attr.ib(init=True, default=attr.Factory(lambda self: OrderedDict([(variable_dict['variable'], []) for variable_dict in self._variables]), takes_self=True))

    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, variables):
        self._variables = variables

    @property
    def valid_variables(self):
        return [self.valid_encoding(x) for x in self._variables]

    def valid_encoding(self, feature):
        return feature.valid_encoding(self.datapoints, self._feature_vectors[feature.variable])

    def update(self, subject: Subject) -> None:
        self._feature_vectors[subject.variable] = subject.columns


@attr.s
class FeatureManager:
    _feature_configuration = attr.ib(init=True)
    subject = attr.ib(init=True, default=Subject([]))

    @property
    def feature_configuration(self):
        return self._feature_configuration

    @feature_configuration.setter
    def feature_configuration(self, feature_configuration):
        self._feature_configuration = FeatureConfiguration(feature_configuration)
