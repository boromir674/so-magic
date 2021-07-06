from abc import ABC, abstractmethod
from functools import reduce
import attr
import pandas as pd

from so_magic.utils import SubclassRegistry


class FillerInterface(ABC):
    @abstractmethod
    def fill(self, *args, **kwargs):
        raise NotImplementedError


class FillerFactoryType(type):

    @classmethod
    def create(mcs, *args, **kwargs) -> FillerInterface:
        raise NotImplementedError


class FillerFactoryClassRegistry(metaclass=SubclassRegistry): pass


@FillerFactoryClassRegistry.register_as_subclass('static')
class StaticDataFiller(FillerInterface):
    def __init__(self, *args, **kwargs) -> None:
        self._variable = args[1]
        if callable(kwargs.get('value')):
            self._fct = kwargs['value']
        else:
            self._fct = self._variable.data_type
            print('\n----->', self._fct, type(self._fct))

    def replace_missing_with_true_zero(self, value, true_zero):
        try:
            if pd.isnull(value):  # True for both np.nan and None
                return true_zero
        except ValueError:
            pass
        return value

    def fill(self, *args, **kwargs):
        datapoints = args[0]
        datapoints.observations[str(self._variable)] = datapoints.observations[str(self._variable)].map(lambda a: self.replace_missing_with_true_zero(a, self._fct()))


@attr.s
class FillerFactory:
    filler_factory_classes_registry = attr.ib(default=attr.Factory(lambda: FillerFactoryClassRegistry))
    def create(self, datapoints, variable, value=None):
        key = 'static'
        return self.filler_factory_classes_registry.create(key, datapoints, variable, value=value)


@attr.s
class MagicFillerFactory:
    filler_factory = attr.ib(init=False, default=attr.Factory(FillerFactory))

    def create(self, datapoints, variable, value=None):
        return self.filler_factory.create(datapoints, variable, value=value)
