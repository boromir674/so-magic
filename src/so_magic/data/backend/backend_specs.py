import attr

from so_magic.utils import SubclassRegistry


class EngineTabularRetriever(metaclass=SubclassRegistry): pass


class EngineTabularIterator(metaclass=SubclassRegistry): pass


class EngineTabularMutator(metaclass=SubclassRegistry): pass


@attr.s
class BackendSpecifications:
    name_abbreviation = attr.ib(init=True)
    name = attr.ib(init=True, default=attr.Factory(lambda self: self.name_abbreviation, takes_self=True))

    def __call__(self, *args, **kwargs):
        backend = args[0]
        backend.retriever = EngineTabularRetriever.subclasses[self.name_abbreviation]
        backend.iterator = EngineTabularIterator.subclasses[self.name_abbreviation]
        backend.mutator = EngineTabularMutator.subclasses[self.name_abbreviation]
        backend.id = self.name_abbreviation

    @classmethod
    def from_dict(cls, a_dict):
        return BackendSpecifications(a_dict['id'], a_dict.get('name', a_dict['id']))
