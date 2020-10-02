import attr
from so_magic.utils import Observer


@attr.s
class CommandsAccumulator(Observer):
    """"""
    commands = attr.ib(init=False, default={})

    def update(self, subject) -> None:
        self.commands[getattr(subject, 'name', str(subject.state))] = subject.state

    def __contains__(self, item):
        return item in self.commands

@attr.s
class CommandGetter:
    _commands_accumulator = attr.ib(init=True, default=CommandsAccumulator())

    @property
    def accumulator(self):
        return self._commands_accumulator

    def __getattr__(self, item):
        if item not in self._commands_accumulator.commands:
            raise KeyError(f"Item '{item}' not found in [{', '.join(str(_) for _ in self._commands_accumulator.commands.keys())}]")
        return self._commands_accumulator.commands[item]


@attr.s
class CommandsManager:
    """[summary]

    Args:
        prototypes (dict, optional): initial prototypes to be supplied
        command_factory (callable, optional): a callable that returns an instance of Command
    """
    _commands_getter = attr.ib(init=True, default=CommandGetter())

    @property
    def command(self):
        return self._commands_getter

    @property
    def commands_dict(self):
        return self._commands_accumulator.commands
