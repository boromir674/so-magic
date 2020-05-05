from abc import ABC, abstractmethod


class FeatureInterface(ABC):
    @abstractmethod
    def values(self, dataset):
        raise NotImplementedError

#### HELPERS
def _list_validator(self, attribute, value):
    if not type(value) == list:
        raise ValueError(f'Expected a list; instead a {type(value).__name__} was given.')

def _string_validator(self, attribute, value):
    if not type(value) == str:
        raise ValueError(f'Expected a string; instead a {type(value).__name__} was given.')


class AbstractFeature(FeatureInterface, ABC):
    def nb_unique(self):
        pass


@attr.s
class BaseFeature(AbstractFeature):
    id = attr.ib(init=True)

    def values(self, dataset):
        """A default implementation of the values method"""
        return dataset[self.id]

@attr.s
class FeatureFunction(BaseFeature):
    function = attr.ib(init=True, default=None)
    name = attr.ib(init=True, default=attr.Factory(lambda self: self.id, takes_self=True))

    def values(self, dataset):
        return self.function(dataset)

    @property
    def index(self):
        return self.id

    @property
    def state(self):
        return FeatureState(self.id, self.function)


@attr.s
class StateMachine:
    states = attr.ib(init=True)
    init_state = attr.ib(init=True)
    _current = attr.ib(init=False, default=attr.Factory(lambda self: self.init_state, takes_self=True))

    @property
    def current(self):
        return self._current

    def update(self, *args, **kwargs):
        if 1 < len(args):
            self.states[args[0]] = args[1]
            self._current = args[0]
        elif 0 < len(args):
            if args[0] in self.states:
                self._current = args[0]
            else:
                raise RuntimeError(f"Requested to set the current state to '{args[0]}', it is not in existing [{', '.join(sorted(self.states))}]")

    @property
    def state(self):
        """Construct an object representing the current state"""
        return FeatureState(self._current, self.state[self._current])


@attr.s
class TrackingFeature:
    feature = attr.ib(init=True)
    sm = attr.ib(init=True)

    @classmethod
    def from_extractor(cls, an_id, function):
        return TrackingFeature(FeatureFunction(an_id, function), StateMachine({'raw': function}, 'raw'))

    def values(self, dataset):
        return self.feature.function(dataset)

    @property
    def index(self):
        return self.feature.id

    @property
    def state(self):
        return self.sm.state

    def update(self, *args, **kwargs):
        self.sm.update(*args, **kwargs)


@attr.s
class FeatureState:
    key = attr.ib(init=True)
    reporter = attr.ib(init=True)
    def __str__(self):
        return self.key


@attr.s
class FeatureIndex:
    keys = attr.ib(init=True, validator=_list_validator)
