from abc import ABCMeta, abstractmethod, ABC

__all__ = ['NominalVariableType', 'OrdinalVariableType', 'IntervalVariableType', 'RatioVariableType', 'VariableTypeFactory']

class VariableType(ABC):
    """
    """
    encoded_allowed = []

    subclasses = {}

    @classmethod
    def register_as_subclass(cls, variable_type):
        def wrapper(subclass):
            cls.subclasses[variable_type] = subclass
            return subclass

        return wrapper

    @classmethod
    def create(cls, variable_type, *args, **kwargs):
        if variable_type not in cls.subclasses:
            raise ValueError('Bad "VariableType" \'{}\''.format(variable_type))
        return cls.subclasses[variable_type](*args, **kwargs)


########
class CategoricalVariableType(VariableType, ABC):
    """Categorical/discrete variable; either 'nominal' or 'ordinal'"""
    pass

@VariableType.register_as_subclass('nominal')
class NominalVariableType(CategoricalVariableType):
    """Nominal variable; discrete variables with undefined ordering; eg country-names"""

    pass
@VariableType.register_as_subclass('ordinal')
class OrdinalVariableType(CategoricalVariableType):
    """Ordinal variable; discrete variables with a defined ordering; eg days-of-the-week"""


########
class NumericalVariableType(VariableType, ABC):
    """Numerical/continuous variables; either 'interval' or 'ratio'"""
    pass

@VariableType.register_as_subclass('interval')
class IntervalVariableType(NumericalVariableType):
    """Interval variable; numerical variable where differences are interpretable; supported operations: [+, -]; no true zero; eg temperature in centigrade (ie Celsius)"""
    pass

@VariableType.register_as_subclass('ratio')
class RatioVariableType(NumericalVariableType):
    """Ratio variable; numerical variable where all operations are supported (+, -, *, /) and true zero is defined; eg weight"""
    pass


class VariableTypeFactory:
    @staticmethod
    def infer(datapoints, attribute, sortable=True, ratio=None):
        """
        Semi-automatic identification; requires some input to assist;
        """
        numerical = datapoints.get_numerical_attributes()
        if attribute in numerical:
            #
            # TODO if all integers -> probably interval
            # TODO if there are negative values -> probably ratio
            if ratio:
                return RatioVariableType()
            return IntervalVariableType()
        if attribute not in set(datapoints.attributes) - set(numerical):
            raise Exception(
                f"The '{attribute}' attribute was not found in the datapoints variables/attributes [{', '.join(str(_ for _ in datapoints.attributes))}].")
        if sortable:
            # TODO change the signature since distinction between nominal and ordinal requires domain knowledge;
            #  requires humman input
            return OrdinalVariableType()
        return NominalVariableType()

    @staticmethod
    def create(variable_type: str, *args, **kwargs):
        return VariableType.create(variable_type, *args, **kwargs)