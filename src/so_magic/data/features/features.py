from abc import ABC, abstractmethod
import attr
from so_magic.data.variables.types import VariableTypeFactory


class AttributeReporter(ABC):
    """A class implementing this interface has the ability to report information on an attribute/variable
    of some structured data (observations)
    """
    @abstractmethod
    def values(self, datapoints, attribute, **kwargs):
        """Call to get the values ([N x 1] vector) of all datapoints (N x D) corresponding to the input variable/attribute.

        Args:
            datapoints (Datapoints): [description]
            attribute (str): [description]

        Return:
            (numpy.ndarray): the values in a [N x 1] vector
        """
        raise NotImplementedError

    @abstractmethod
    def variable_type(self, datapoints, attribute, **kwargs):
        """Call to get the variable type of the datapoints, given the attribute.

        Args:
            datapoints (Datapoints): [description]
            attribute (str): [description]

        Return:
            (str): [description]
        """
        raise NotImplementedError

    @abstractmethod
    def value_set(self, datapoints, attribute, **kwargs):
        raise NotImplementedError


class BaseAttributeReporter(AttributeReporter):

    def values(self, datapoints, attribute, **kwargs):
        return datapoints[attribute]

    def variable_type(self, datapoints, attribute, **kwargs):
        return VariableTypeFactory.infer(datapoints, attribute, **kwargs)

    def value_set(self, datapoints, attribute, **kwargs):
        return set([_ for _ in datapoints.column(attribute)])


#### HELPERS
def _list_validator(self, attribute, value):
    if not type(value) == list:
        raise ValueError(f'Expected a list; instead a {type(value).__name__} was given.')

def _string_validator(self, attribute, value):
    if not type(value) == str:
        raise ValueError(f'Expected a string; instead a {type(value).__name__} was given.')


@attr.s
class AttributeReporter:
    label = attr.ib(init=True)
    reporter = attr.ib(init=True, default=BaseAttributeReporter())

    def values(self, datapoints):
        """A default implementation of the values method"""
        return self.reporter.values(datapoints, self.label)

    def variable_type(self, datapoints):
        """A default implementation of the values method"""
        return self.reporter.variable_type(datapoints, self.label)

    def value_set(self, datapoints):
        return self.reporter.value_set(datapoints, self.label)

    def __str__(self):
        return self.label

@attr.s
class FeatureState:
    key = attr.ib(init=True)
    reporter = attr.ib(init=True)

    def __str__(self):
        return self.key


@attr.s
class FeatureFunction:
    """Example: Assume we have a datapoint v = [v_1, v_2, .., v_n, and 2 feature functions f_1, f_2\n
    Then we can produce an encoded vector (eg to feed for training a ML model) like: encoded_vector = [f_1(v), f_2(v)]
    """
    function = attr.ib(init=True)
    @function.validator
    def is_callable(self, attribute, value):
        if not callable(value):
            raise ValueError(f"Expected a callable object; instead {type(value)} was given.")
        if value.func_code.co_argcount < 1:
            raise ValueError(f"Expected a callable that takes at least 1 argument; instead a callable that takes no arguments was given.")

    label = attr.ib(init=True, default=None)
    @label.validator
    def is_label(self, attribute, value):
        if value is None:
            self.label = self.function.func_name

    def values(self, dataset):
        return self.function(dataset)

    @property
    def state(self):
        return FeatureState(self.label, self.function)


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
        return FeatureState(self._current, self.states[self._current])


@attr.s
class TrackingFeature:
    feature = attr.ib(init=True)
    state_machine = attr.ib(init=True)
    variable_type = attr.ib(init=True, default=None)

    @classmethod
    def from_callable(cls, a_callable, label=None, variable_type=None):
        """Construct a feature that has one extract/report capability. Input id is correlated to the features position on the vector (see FeatureFunction above)"""
        return TrackingFeature(FeatureFunction(a_callable, label), StateMachine({'raw': a_callable}, 'raw'), variable_type)

    def values(self, dataset):
        return self.state_machine.state.reporter(dataset)

    def label(self):
        return self.feature.label

    @property
    def state(self):
        """Returns the current state"""
        return self.state_machine.state

    def update(self, *args, **kwargs):
        self.state_machine.update(*args, **kwargs)


@attr.s
class FeatureIndex:
    keys = attr.ib(init=True, validator=_list_validator)


class PhiFeatureFunction:
    def __call__(self, *args, **kwargs):
        raise NotImplementedError