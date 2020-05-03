import re
import attr


@attr.s(str=True, repr=True)
class Strain:
    id = attr.ib(init=True)
    name = attr.ib(init=True)
    type = attr.ib(init=True)
    flavors = attr.ib(init=True, default=None)
    effects = attr.ib(init=True, default=None)
    medical = attr.ib(init=True, default=None)
    negatives = attr.ib(init=True, default=None)
    parents = attr.ib(init=True, default=None)
    stretch = attr.ib(init=True, default=None)
    flowering = attr.ib(init=True, default=None)
    yield_ = attr.ib(init=True, default=None)
    height = attr.ib(init=True, default=None)
    difficulty = attr.ib(init=True, default=None)
    images = attr.ib(init=True, default=None)
    description = attr.ib(init=True, default=None)

    @classmethod
    def new(cls, *args, **kwargs):
        return Strain()

    @classmethod
    def from_dict(cls, json_ready_dict):
        return Strain(
            json_ready_dict['_id'],
            json_ready_dict['name'],
            json_ready_dict['type'],
            json_ready_dict.get('flavors', []),
            json_ready_dict.get('effects', {}),
            json_ready_dict.get('medical', {}),
            json_ready_dict.get('negatives', {}),
            json_ready_dict.get('parents', []),
            *[cls._b([x, json_ready_dict.get(x, 'NaN')]) for x in ('stretch', 'flowering', 'yield', 'height', 'difficulty')],
            json_ready_dict.get('images', {}),
            json_ready_dict.get('description', {}))

    @classmethod
    def _b(cls, x):
        return {'NaN': lambda z: None}.get(x[1], lambda y: GrowInfo.create(*y))(x)


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


@attr.s
class PositiveRange:
    range = attr.ib(init=True)
    @range.validator
    def _lower_sanity(self, attribute, value):
        if float(self.range[0]) < 0:
            raise ValueError("Lower: {}. It should be >= 0")
        self.range = Range(*value)


######################## GROW INFO ###################################

@attr.s
class GrowInfo:
    subclasses = {}

    @classmethod
    def register_subclass(cls, grow_info_subcategory):
        def decorator(subclass):
            cls.subclasses[grow_info_subcategory] = subclass
            return subclass
        return decorator

    @classmethod
    def create(cls, grow_info_subcategory, *args, **kwargs):
        if grow_info_subcategory not in cls.subclasses:
            raise ValueError('Bad grow_info_subcategory \'{}\''.format(grow_info_subcategory))
        return cls.subclasses[grow_info_subcategory](*args, **kwargs)

    @classmethod
    def _construct(cls, grow_info_subcategory, *args, **kwargs):
        if grow_info_subcategory not in cls.subclasses:
            raise ValueError('Bad grow_info_subcategory \'{}\''.format(grow_info_subcategory))
        return cls.subclasses[grow_info_subcategory](*args, **kwargs)


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
                print('AAA {}'.format(value))
                self.range = PositiveRange(0, float(re.search(r'\d+', value).group()))
            elif value[0] == '>':
                print('BBB {}'.format(value))
                self.range = PositiveRange([float(re.search(r'\d+', value).group()), float('inf')])
            else:
                print('CCC {}'.format(value))
                self.range = PositiveRange([re.search(r'(\d+)-(\d+)', value).groups()])
        elif len(value) == 2:
            print('DDD {}'.format(value))
            self.range = PositiveRange(value)
        else:
            raise ValueError("Input data for stretch should be a string or a 2-element list/tuple")


@GrowInfo.register_subclass('flowering')
@attr.s
class FloweringField(GrowInfo):
    """Flowering period in weeks;
        eg: 7-9, 10-12"""
    range = attr.ib(init=True)
    @range.validator
    def _weeks_range(self, attribute, value):
        if type(value) == str:
            if value[0] == '<':
                self.range = PositiveRange([0, float(re.search(r'\d+', value).group())])
            elif value[0] == '>':
                self.range = PositiveRange([float(re.search(r'\d+', value).group()), float('inf')])
            else:
                self.range = PositiveRange(re.search(r'(\d+)-(\d+)', value).groups())
        elif len(value) == 2:
            self.range = PositiveRange(value)
        else:
            raise RuntimeError("Input data for flowering should be either a string or a 2-element list/tuple")

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
