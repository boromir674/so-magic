# from __future__ import annotations
from abc import ABCMeta, abstractmethod, ABC
from .interfaces import Component, Visitor


class VariableType(Component, metaclass=ABCMeta):
    """
    Each Concrete Component must implement the `accept` method in such a way
    that it calls the visitor's method corresponding to the component's class.
    """
    pass

########
class CategoricalVariableType(VariableType, ABC):
    """Categorical/discrete variable; either 'nominal' or 'ordinal'"""
    pass
##
class NominalVariable(CategoricalVariableType):
    """Nominal variable; discrete variables with undefined ordering; eg country-names"""
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_nominal(self)


class OrdinalVariable(CategoricalVariableType):
    """Ordinal variable; discrete variables with a defined ordering; eg days-of-the-week"""
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_ordinal(self)


########
class NumericalVariableType(VariableType, ABC):
    """Numerical/continuous variables; either 'interval' or 'ratio'"""
    pass
##
class Interval(NumericalVariableType):
    """Interval variable; numerical variable where differences are interpretable; supported operations: [+, -]; no true zero; eg temperature in centigrade (ie Celsius)"""
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_interval(self)


class Ratio(NumericalVariableType):
    """Ratio variable; numerical variable where all operations are supported (+, -, *, /) and true zero is defined; eg weight"""

    def accept(self, visitor: Visitor) -> None:
        visitor.visit_ratio(self)


#################################################

class FeatureVisitor(Visitor):
    """
    The Visitor Interface declares a set of visiting methods that correspond to
    component classes. The signature of a visiting method allows the visitor to
    identify the exact class of the component that it's dealing with.
    """

    @abstractmethod
    def visit_nominal(self, element: NominalVariable) -> None:
        raise NotImplementedError

    @abstractmethod
    def visit_ordinal(self, element: OrdinalVariable) -> None:
        raise NotImplementedError

    @abstractmethod
    def visit_interval(self, element: Interval) -> None:
        raise NotImplementedError

    @abstractmethod
    def visit_ratio(self, element: Ratio) -> None:
        raise NotImplementedError

