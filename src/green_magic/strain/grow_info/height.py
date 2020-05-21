import attr
from .base_info import GrowInfo
from .helpers import PositiveRange

@GrowInfo.register_subclass('height')
@attr.s
class HeightField(GrowInfo):
    """Plant height measured in meters;
        eg: <.75, .76-2, >2"""
    range = attr.ib(init=True)
    @range.validator
    def _height_range(self, attribute, value):
        if type(value) == str:
            if value[0] == '<':
                self.range = PositiveRange(0, float(value.split(' ')[-1]))
            elif value[0] == '>':
                self.range = PositiveRange(float(value.split(' ')[-1]), float('inf'))
            else:
                self.range = PositiveRange(float(value.split('-')[0]), float(value.split('-')[1].split(' ')[0]))
        elif len(value) == 2:
            self.range = PositiveRange(value)
        else:
            raise RuntimeError("Input data for flowering should be either a string or a 2-element list/tuple")
