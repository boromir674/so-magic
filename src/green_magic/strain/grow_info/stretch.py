import attr
from .base_info import GrowInfo
from .helpers import PositiveRange


@GrowInfo.register_subclass('stretch')
@attr.s
class StretchField(GrowInfo):
    """Stretch output percentage-wise:
        eg: 100-200, >200, <100"""
    range = attr.ib(init=True)
    @range.validator
    def _stretch_range(self, attribute, value):
        if type(value) == str:
            if value[0] == '<':
                self.range = PositiveRange(0, float(re.search(r'\d+', value).group()))
            elif value[0] == '>':
                self.range = PositiveRange(*[float(re.search(r'\d+', value).group()), float('inf')])
            else:
                self.range = PositiveRange(*[re.search(r'(\d+)-(\d+)', value).groups()])
        elif len(value) == 2:
            self.range = PositiveRange(value)
        else:
            raise ValueError("Input data for stretch should be a string or a 2-element list/tuple")
