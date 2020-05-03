from abc import abstractmethod, ABC


class FeatureInterface(ABC):
    @property
    @abstractmethod
    def nb_unique(self):
        raise NotImplementedError




@attr.s
class Features:
    feats = attr.ib(init=True)
    @feats.validator
    def list_validator(self, attribute, value):
        if not type(value) == list:
            raise ValueError(f'Expected a list, instead a {type(value).__name__} was give.')

    def __getitem__(self, item):
        return self.feats[item]

    def __iter__(self):
        return iter((feat.id, feat) for feat in self.feats)


# def effects_f(item):
#     return item['effects']
#
#
# def medical_f(item):
#     return item['medical']
#
#
# def negatives_f(item):
#     return item['negatives']
#
#
# def flavors_f(item):
#     return item['flavors']
#
#
# def parents_f(item):
#     return item['parents']
#
#
# def difficulty_f(item):
#     return str(item['grow_info']['difficulty'])
#
#
# def height_f(item):
#     return str(item['grow_info']['height'])
#
#
# def yield_f(item):
#     return str(item['grow_info']['yield'])
#
#
# def flowering_f(item):
#     return str(item['grow_info']['flowering'])
#
#
# def stretch_f(item):
#     return str(item['grow_info']['stretch'])
