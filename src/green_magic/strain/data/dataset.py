import attr


@attr.s(str=True, repr=True)
class Dataset:
    datapoints = attr.ib(init=True)
    name = attr.ib(init=True, default=None)
    size = attr.ib(init=False, default=attr.Factory(lambda self: len(self.datapoints), takes_self=True))
    _features = attr.ib(init=True, default=[])
    handler = attr.ib(init=True, default=None)

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, features):
        self._features = features


@attr.s
class Datapoints:
    observations = attr.ib(init=True)

    def __getitem__(self, item):
        return self.observations[item]

    def __iter__(self):
        return iter(self.observations)

    def __len__(self):
        return len(self.observations)

    @classmethod
    def from_df(cls, df):
        return Datapoints(df)
#
# @attr.s
# class TabularData(Datapoints):
#     data = attr.ib(init=True)
#
#
#     def add_state(self, data, feature, state, columns=None):
#
#         return



@attr.s
class FeatureList:
    features = attr.ib(init=True)

    def __getitem__(self, item):
        return self.features[item]

    def __len__(self):
        return len(self.features)