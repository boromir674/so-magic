import attr
from green_magic.utils import GenericMediator, BaseComponent, ObjectRegistry, Observer
from enum import Enum


class MediatorEvent(Enum):
    A = 'A'
    B = 'B'
    C = 'C'


class DataMediator(GenericMediator):
    def __init__(self, *args, **kwargs):
        self.events = kwargs.get('events', {})

    def notify(self, sender: object, event: str) -> None:
        pass


class Phis(ObjectRegistry, Observer):
    def __getattr__(self, item):
        return self.objects[item]
    def update(self, subject):
        self.add(subject.name, subject.state)


@attr.s
class DataManager:
    commands_manager = attr.ib(init=True)
    backend = attr.ib(init=True)
    mediator = attr.ib(init=False, default=None)
    built_phis = attr.ib(init=False, default=Phis())

    def __attrs_post_init__(self):
        self.mediator = DataMediator(self.commands_manager, self.backend)

    @property
    def phis(self):
        return self.built_phis

    @property
    def commands(self):
        return self.commands_manager.commands_dict

    @property
    def command(self):
        return self.commands_manager.command