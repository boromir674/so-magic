from abc import ABC, abstractmethod
import attr
from so_magic.utils import SubclassRegistry


class EncoderInterface(ABC):
    @abstractmethod
    def encode(self, *args, **kwargs):
        raise NotImplementedError


class EncoderFactoryType(type):

    @classmethod
    def create(mcs, *args, **kwargs) -> EncoderInterface:
        raise NotImplementedError


# class NominalVariableEncoderFactory:
#     @classmethod
#     def create(cls, *args, **kwargs) -> EncoderInterface:



@attr.s(slots=True)
class NominalAttributeEncoder(EncoderInterface, ABC):
    """Encode the observations of a categorical nominal variable.

    The client code can supply the possible values for the nominal variable, if known a priori.
    The possible values are stored in the 'values_set' attribute/property. If they are not supplied
    they should be computed at runtime (when running the encode method).

    It also defines and stores the string identifiers for each column produced in the 'columns attribute/property.

    Args:
        values_set (list): the possible values of the nominal variable observations, if known a priori
    """
    values_set: list = attr.ib(default=attr.Factory(list))
    columns: list = attr.ib(init=False, default=attr.Factory(list))


class EncoderFactoryClassRegistry(metaclass=SubclassRegistry): pass

from functools import reduce
import pandas as pd


@EncoderFactoryClassRegistry.register_as_subclass('nominal_list')
class OneHotListEncoder(EncoderInterface):
    binary_transformer = {True: 1.0, False: 0.0}
    column_name_joiner = '_'
    def __init__(self, *args, **kwargs) -> None:
        pass
    def encode(self, *args, **kwargs):
        datapoints = args[0]
        attribute = args[1]
        print('ATRTRBUTE', attribute)
        print('STR', str(attribute))
        cc = [_ for _ in datapoints.observations[str(attribute)]] 
        print('LEN1', len(cc))
        c = [_ for _ in cc if isinstance(_, list)]
        print('LEN2', len(c))
        self.values_set = reduce(lambda i, j: set(i).union(set(j)),
                                 c)
        self.columns = sorted([f'{str(attribute)}{self.column_name_joiner}{x}' for x in self.values_set])
        return pd.DataFrame([self._yield_vector(datarow, str(attribute)) for index, datarow in datapoints.iterrows()],
                            columns=self.columns)

    def _yield_vector(self, datarow, attribute):
        decision = {True: self._encode, False: self._encode_none}
        return decision[isinstance(datarow[str(attribute)], list)](datarow, str(attribute))

    def _encode(self, datarow, attribute):
        return [self.binary_transformer[column in datarow[str(attribute)]] for column in sorted(self.values_set)]

    def _encode_none(self, _datarow, _attribute):
        return [0.0] * len(self.values_set)
    
    def get_feature_names(self):
        return self.columns



@EncoderFactoryClassRegistry.register_as_subclass('nominal_str')
class OneHotStringEncoder(EncoderInterface):
    binary_transformer = {True: 1.0, False: 0.0}
    column_name_joiner = '_'
    def __init__(self, *args, **kwargs) -> None:
        pass
    def encode(self, *args, **kwargs):
        datapoints = args[0]
        attribute = args[1]
        print('ATRTRBUTE', attribute)
        print('STR', str(attribute))
        c = [x for x in datapoints.observations[str(attribute)] if isinstance(x, str)]
        self.values_set = {value for value in c}
        self.columns = sorted([f'{str(attribute)}{self.column_name_joiner}{x}' for x in self.values_set])
        return pd.DataFrame([self._yield_vector(datarow, str(attribute)) for index, datarow in datapoints.iterrows()],
                            columns=self.columns)

    def _yield_vector(self, datarow, attribute):
        decision = {True: self._encode, False: self._encode_none}
        return decision[isinstance(datarow[str(attribute)], str)](datarow, str(attribute))

    def _encode(self, datarow, attribute):
        return [self.binary_transformer[variable_value == datarow[str(attribute)]] for variable_value in sorted(self.values_set)]

    def _encode_none(self, _datarow, _attribute):
        return [0.0] * len(self.values_set)

    def get_feature_names(self):
        return self.columns


@attr.s
class EncoderFactory:
    encoder_factory_classes_registry = attr.ib(default=attr.Factory(lambda: EncoderFactoryClassRegistry))
    def create(self, datapoints, variable, scheme='auto'):
        key = self.get_key(variable)
        return self.encoder_factory_classes_registry.create(key, datapoints, variable, scheme='auto')

    def get_key(self, variable):
        return f'{str(variable.type).lower()}_{str(variable.data_type.__name__)}'


@attr.s
class MagicEncoderFactory:
    encoder_factory = attr.ib(init=False, default=attr.Factory(lambda: EncoderFactory()))

    def create(self, datapoints, variable, scheme='auto'):
        return self.encoder_factory.create(datapoints, variable, scheme='auto')
