import attr
from .base_info import GrowInfo
from .helpers import PositiveRange

@GrowInfo.register_subclass('yield')
@attr.s
class YieldField(GrowInfo):
    """Yield in grams per square meter; gr/m^2
        eg: 251-500, 100-250, 40-99"""
    range = attr.ib(init=True)
    @range.validator
    def _yield_range(self, attribute, value):
        if type(value) == str:
            self.range = PositiveRange(value.split('-'))
        elif len(value) == 2:
            self.range = PositiveRange(value)
        else:
            raise RuntimeError("Input data for flowering should be either a string or a 2-element list/tuple")
