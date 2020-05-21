import attr


@attr.s(cmp=False)
class Range:
    lower = attr.ib(init=True)
    upper = attr.ib(init=True)
    @upper.validator
    def _range_sanity(self, attribute, value):
        if value <= self.lower:
            raise ValueError("Lower: {}, upper: {}. Cannot represent a valid range")

    def __eq__(self, other):
        return self.lower == other.lower and self.upper == other.upper

    def __ne__(self, other):
        return self.lower != other.lower or self.upper != other.upper

    def __le__(self, other):
        return self.upper <= other.lower or self == other

    def __lt__(self, other):
        return self.upper <= other.lower

    def __ge__(self, other):
        return other.upper <= self.lower or self == other

    def __gt__(self, other):
        return other.upper <= self.lower

    def __len__(self):
        return 2

    def __getitem__(self, item):
        if item == 0:
            return self.lower
        if item == 1:
            return self.upper
        raise IndexError


class PositiveRange(Range):
    def __new__(cls, *args, **kwargs):
        if float(args[0]) < 0:
            raise ValueError("Expected the lower bound to be a positive number. Instead {} was given.".format(args[0]))
        return super().__new__(cls)
