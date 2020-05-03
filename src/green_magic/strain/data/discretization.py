from abc import ABC
import attr
import copy


class DiscretizerInterface(ABC):
    def discretize(self, *args, **kwargs):
        raise NotImplementedError


class AbstractDiscretizer(DiscretizerInterface):
    def discretize(self, *args, **kwargs):
        raise NotImplementedError


class BinnerInterface(ABC):
    def bin(self, values, nb_bins):
        raise NotImplementedError


@attr.s
class BaseDiscretizer(AbstractDiscretizer):
    bin = attr.ib(init=True)
    @bin.validator
    def validate_bin_function(self, attribute, value):
        if not callable(value):
            raise ValueError(f'Expected a callable object, instead a {type(value).__name__} was given.')

    def discretize(self, *args, **kwargs):
        """Expects args: dataset, feature and kwargs; 'nb_bins'."""
        return self.bin(args[1].function(args[0]), kwargs['nb_bins'])


@attr.s
class FeatureDiscretizer(BaseDiscretizer):
    feature = attr.ib(init=True)

    def __call__(self, *args, **kwargs):
        dataset, nb_bins = args[:2]
        return self.bin(self.feature.function(dataset), nb_bins)



class FeatureDiscretizerFactory:
    def categorical(self, feature) -> FeatureDiscretizer:
        raise NotImplementedError

    def numerical(self, feature) -> FeatureDiscretizer:
        raise NotImplementedError
