import re
import attr

from .grow_info import GrowInfo


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
