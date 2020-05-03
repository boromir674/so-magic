import attr
from abc import ABC, abstractmethod


class ValuesExtractor(ABC):
    @abstractmethod
    def values(self, dataset, feature, **kwargs):
        raise NotImplementedError


@attr.s
class BaseValuesExtractor(ValuesExtractor):
    _callable = attr.ib(init=True)
    @_callable.validator
    def is_method(self, attribute, value):
        if not callable(value):
            raise ValueError(f"Expected a callable object, instead {type(value).__name__} was given.")

    def values(self, dataset, feature, **kwargs):
        return self._callable(dataset, feature)
