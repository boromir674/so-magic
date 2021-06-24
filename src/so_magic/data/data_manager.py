import attr
from so_magic.utils import ObjectRegistry, Observer
from .commands_manager import CommandsManager


@attr.s
class Phis(Observer):
    registry: ObjectRegistry = attr.ib(default=attr.Factory(ObjectRegistry))

    def __getattr__(self, item):
        return getattr(self.registry, item)

    def __contains__(self, item):
        return item in self.registry

    def update(self, subject, *args, **kwargs):
        self.registry.add(subject.name, subject.state)


@attr.s
class DataManager:
    engine = attr.ib(init=True)
    _phi_function_class = attr.ib(init=True)
    feature_manager = attr.ib(init=True)

    commands_manager = attr.ib(init=True, default=CommandsManager())
    # mediator = attr.ib(init=False, default=attr.Factory(
    #     lambda self: DataMediator(self.commands_manager, self.backend), takes_self=True))
    built_phis = attr.ib(init=False, default=Phis())

    def __attrs_post_init__(self):
        self.engine.backend.datapoints_factory.subject.attach(self.engine.datapoints_manager)
        self.engine.backend.command_factory.subject.attach(self.commands_manager.command.accumulator)
        self._phi_function_class.subject.attach(self.built_phis)

    @property
    def phis(self):
        return self.built_phis

    @property
    def phi_class(self):
        return self._phi_function_class

    @property
    def commands(self):
        return self.commands_manager.commands_dict

    @property
    def command(self):
        return self.commands_manager.command

    @property
    def datapoints(self):
        return self.engine.datapoints_manager.datapoints
