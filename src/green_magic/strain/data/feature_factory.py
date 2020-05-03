from abc import ABC
import attr

from ..features import FeatureInterface



#### HELPERS

def _list_validator(self, attribute, value):
    if not type(value) == list:
        raise ValueError(f'Expected a list; instead a {type(value).__name__} was given.')

def _string_validator(self, attribute, value):
    if not type(value) == str:
        raise ValueError(f'Expected a string; instead a {type(value).__name__} was given.')



class AbstractFeature(FeatureInterface):

    def nb_unique(self):
        pass

    def values(self, dataset):
        raise NotImplementedError


@attr.s
class BaseFeature(AbstractFeature):
    id = attr.ib(init=True)
    name = attr.ib(init=True, default=attr.Factory(lambda self: self.id, takes_self=True))

    def values(self, dataset):
        """A default implementation of the values method"""
        return dataset[self.id]


@attr.s
class Feature(BaseFeature):
    function = attr.ib(init=True, default=None)
    # variable_type = attr.ib(init=True, default=None)

    def values(self, dataset):
        return self.function(dataset)

    @property
    def index(self):
        return self.id

    @property
    def state(self):
        return FeatureState(self.id, self.function)

@attr.s
class FeatureState:
    key = attr.ib(init=True)
    reporter = attr.ib(init=True)
    def __str__(self):
        return self.key

    @staticmethod
    def current(feature):
        return FeatureState(feature.current, feature.function)

@attr.s
class FeatureIndex:
    keys = attr.ib(init=True, validator=_list_validator)

class FeatureStateFactory:
    @classmethod
    def get_state(cls, *args, **kwargs):
        return FeatureState(args[0], args[1])
    @classmethod
    def current(cls, feature):
        return FeatureState(feature.current, feature.function)

@attr.s
class TrackingFeat(Feature):
    states = attr.ib(init=True, default=attr.Factory(lambda self: {'raw': self.function}, takes_self=True))
    current = attr.ib(init=True, default='raw')

    @property
    def state(self):
        return FeatureState(self.current, self.states[self.current])

    @property
    def index(self):
        return self.id
    # def values(self, dataset):
    #     return self.states[self._current](dataset)

    def update(self, *args, **kwargs):
        if 1 < len(args):
            self.states[args[0]] = args[1]
            self.current, self.function = args[:2]
        elif 0 < len(args):
            if args[0] in self.states:
                self.current = args[0]
                self.function = self.states[self.current]
            else:
                raise RuntimeError(f"Requested to set the current state to '{args[0]}', it is not in existing [{', '.join(sorted(self.states))}]")


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



@attr.s
class Features:
    feats = attr.ib(init=True)
    @feats.validator
    def list_validator(self, attribute, value):
        if not type(value) == list:
            raise ValueError(f'Expected a list, instead a {type(value).__name__} was give.')

    def __getitem__(self, item):
        return self.feats[item]

    def __iter__(self):
        return iter((feat.id, feat) for feat in self.feats)


feat_state_fact = FeatureStateFactory()
