import attr
from .base_info import GrowInfo
from .helpers import PositiveRange


@GrowInfo.register_subclass('difficulty')
@attr.s
class DifficultyField(GrowInfo):
    valid = ['easy', 'medium', 'difficult']
    data = attr.ib(init=True)
    @data.validator
    def _difficulty_value(self, attribute, value):
        if value not in DifficultyField.valid:
            raise ValueError("{} is not in [{}]".format(value, ', '.join(DifficultyField.valid)))

    def __le__(self, other):
        return DifficultyField.valid.index(self.data) <= DifficultyField.valid.index(other.data)

    def __lt__(self, other):
        return DifficultyField.valid.index(self.data) < DifficultyField.valid.index(other.data)

    def __eq__(self, other):
        return self.data == other.data

    def __ne__(self, other):
        return self.data != other.data

    def __ge__(self, other):
        return DifficultyField.valid.index(self.data) >= DifficultyField.valid.index(other.data)

    def __gt__(self, other):
        return DifficultyField.valid.index(self.data) > DifficultyField.valid.index(other.data)
