from abc import abstractmethod, ABC


class FeatureInterface(ABC):
    @property
    @abstractmethod
    def nb_unique(self):
        raise NotImplementedError





# class RawValueExtractor(metaclass=ABCMeta):
#     @classmethod
#     def __subclasshook__(cls, subclass):
#         return hasattr(subclass, 'raw_value') and callable(subclass.raw_value)
#
#     @abstractmethod
#     def raw_value(self, observation):
#         raise NotImplementedError
#
#
#
# #### DICT-LIKE Features ####
#
# class DictLikeExtractor(RawValueExtractor, ABC):
#     subclasses = {}
#     @classmethod
#     def register_subclass(cls, feature):
#         def decorator(subclass):
#             cls.subclasses[feature] = subclass
#             return subclass
#         return decorator
#
#     @classmethod
#     def create(cls, feature, *args, **kwargs):
#         if feature not in cls.subclasses:
#             raise ValueError('Bad feature {} requested for instantiation'.format(feature))
#         return cls.subclasses[feature](*args, **kwargs)
#
#     @classmethod
#     def from_callable(cls, a_callable):
#         return DictLikeExtractor
#
# @DictLikeExtractor.register_subclass
# class NameExtractor(DictLikeExtractor):
#
#     def raw_value(self, observation):
#         return observation['name']
#
# @DictLikeExtractor.register_subclass
# class TypeExtractor(DictLikeExtractor):
#
#     def raw_value(self, observation):
#         return observation['type']
#
#
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
