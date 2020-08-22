from enum import Enum
import attr
from green_magic.utils import GenericMediator, BaseComponent, ObjectRegistry, Observer
from .commands_manager import CommandsManager


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
    backend = attr.ib(init=True)
    commands_manager = attr.ib(init=True, default=CommandsManager())
    mediator = attr.ib(init=False, default=attr.Factory(lambda self: DataMediator(self.commands_manager, self.backend), takes_self=True))
    built_phis = attr.ib(init=False, default=Phis())

    def __attrs_post_init__(self):
        self.backend.engine.__class__.datapoints_factory.subject.attach(self.backend.datapoints_manager)
        self.backend.engine.command_factory.attach(self.commands_manager.command.accumulator)

    @property
    def phis(self):
        return self.built_phis

    @property
    def commands(self):
        return self.commands_manager.commands_dict

    @property
    def command(self):
        return self.commands_manager.command
