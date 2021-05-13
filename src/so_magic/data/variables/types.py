from abc import ABC


__all__ = ['NominalVariableType', 'OrdinalVariableType', 'IntervalVariableType', 'RatioVariableType',
           'VariableTypeFactory']


class VariableType(ABC):
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


@VariableType.register_as_subclass('nominal')
class NominalVariableType(CategoricalVariableType):
    """Nominal variable; discrete variables with undefined ordering; eg country-names"""


@VariableType.register_as_subclass('ordinal')
class OrdinalVariableType(CategoricalVariableType):
    """Ordinal variable; discrete variables with a defined ordering; eg days-of-the-week"""


########
class NumericalVariableType(VariableType, ABC):
    """Numerical/continuous variables; either 'interval' or 'ratio'"""



@VariableType.register_as_subclass('interval')
class IntervalVariableType(NumericalVariableType):
    """Interval numerical variable type

    Variables of type interval have interpretable differences; supported operations: [+, -].
    There is no true zero.

    Example: temperature in Celsius can be measured with an interval variable interval variable

    Interpretable difference:

    10 degrees drop from 30 degrees Celsius actually means 30 - 10 = 20 degrees Celsius

    5 degrees rise 20 degrees Celsius actually means 20 + 5 = 25 degrees Celsius
    degrees Celsius - 10 degrees Celsius = 20 degrees Celsius

    There is no true zero:

    Theoretically we can go plus infinite degrees Celsius and minus infinite

    There is no number that can "eliminate" (even zero has valid Celsius degrees smaller than 0) a temperature
    measurement in Celsius degrees
    """


@VariableType.register_as_subclass('ratio')
class RatioVariableType(NumericalVariableType):
    r"""Ratio numerical variable where all operations are supported (+, -, \*, /) and true zero is defined; eg weight"""


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
                f"The '{attribute}' attribute was not found in the datapoints variables/attributes "
                f"[{', '.join(str(_ for _ in datapoints.attributes))}].")
        if sortable:
            # TODO change the signature since distinction between nominal and ordinal requires domain knowledge;
            #  requires humman input
            return OrdinalVariableType()
        return NominalVariableType()

    @staticmethod
    def create(variable_type: str, *args, **kwargs):
        return VariableType.create(variable_type, *args, **kwargs)
