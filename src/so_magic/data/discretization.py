from abc import ABC
import attr
from so_magic.utils import SubclassRegistry


class DiscretizerInterface(ABC):
    def discretize(self, *args, **kwargs):
        raise NotImplementedError


class AbstractDiscretizer(DiscretizerInterface):
    def discretize(self, *args, **kwargs):
        raise NotImplementedError


def validate_bin_function(_self, _attribute, value):
    if not callable(value):
        raise ValueError(f'Expected a callable object, instead a {type(value).__name__} was given.')

@attr.s
class BaseDiscretizer(AbstractDiscretizer):
    binner = attr.ib(init=True, validator=validate_bin_function)

    def discretize(self, *args, **kwargs):
        """Expects args: dataset, feature and kwargs; 'nb_bins'."""
        dataset, feature, nb_bins = args[0], args[1], args[2]
        return self.binner(feature.values(dataset), nb_bins)


@attr.s
class FeatureDiscretizer(BaseDiscretizer):
    feature = attr.ib(init=True)

    def discretize(self, *args, **kwargs):
        """Expects args: dataset, nb_bins."""
        return super().discretize(args[0], self.feature, args[1])

@attr.s
class FeatureDiscretizerFactory:
    binner_factory = attr.ib(init=True)

    def categorical(self, feature, **kwargs) -> FeatureDiscretizer:
        binner_type = 'same-length'
        if kwargs.get('quantisized', False):
            binner_type = 'quantisized'
        return FeatureDiscretizer(self.binner_factory.create_binner(binner_type), feature)

    def numerical(self, feature, **kwargs) -> FeatureDiscretizer:
        binner_type = 'same-length'
        if kwargs.get('quantisized', False):
            binner_type = 'quantisized'
        return FeatureDiscretizer(self.binner_factory.create_binner(binner_type), feature)


#########################################

class BinnerInterface(ABC):
    def bin(self, values, nb_bins):
        raise NotImplementedError


class BaseBinner(BinnerInterface):

    def bin(self, values, nb_bins):
        """It is assumed numerical (ratio or interval) variable or ordinal (not nominal) categorical variable."""
        raise NotImplementedError


class BinnerClass(metaclass=SubclassRegistry): pass


class BinnerFactory:
    parent_class = BinnerClass

    def equal_length_binner(self, *args, **kwargs) -> BaseBinner:
        raise NotImplementedError

    def quantisized_binner(self, *args, **kwargs) -> BaseBinner:
        raise NotImplementedError

    def create_binner(self, *args, **kwargs) -> BaseBinner:
        raise NotImplementedError
