from abc import ABCMeta, abstractmethod, ABC

__all__ = ['NominalVariableType', 'OrdinalVariableType', 'IntervalVariableType', 'RatioVariableType']

class VariableType(ABC):
    """
    """
    encoded_allowed = []


########
class CategoricalVariableType(VariableType, ABC):
    """Categorical/discrete variable; either 'nominal' or 'ordinal'"""
    pass

class NominalVariableType(CategoricalVariableType):
    """Nominal variable; discrete variables with undefined ordering; eg country-names"""
    # data = {list: lambda x: all(el in [0, 1] for )}
    # def check(cls, dataset, feature):
    pass

class OrdinalVariableType(CategoricalVariableType):
    """Ordinal variable; discrete variables with a defined ordering; eg days-of-the-week"""


########
class NumericalVariableType(VariableType, ABC):
    """Numerical/continuous variables; either 'interval' or 'ratio'"""
    pass

class IntervalVariableType(NumericalVariableType):
    """Interval variable; numerical variable where differences are interpretable; supported operations: [+, -]; no true zero; eg temperature in centigrade (ie Celsius)"""
    pass


class RatioVariableType(NumericalVariableType):
    """Ratio variable; numerical variable where all operations are supported (+, -, *, /) and true zero is defined; eg weight"""
    pass
