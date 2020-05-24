from __future__ import annotations
from abc import ABC, abstractmethod
import attr


class Command(ABC):
    """The Command interface declares a method for executing a command."""

    @abstractmethod
    def execute(self) -> None:
        pass


@attr.s
class CommandHistory:
    """ The global command history is just a stack."""
    _history = attr.ib(init=False, default=[])
    @_history.validator
    def validate_history(self, attribute, value):
        if type(value) != list:
            raise ValueError(f"Expected a list, instead a {type(value).__name__} was given")

    def push(self, c: Command):
        self._history.append(c)

    def pop(self) -> Command:
        return self._history.pop(0)


@attr.s
class MultiCommand(Command):
    _commands = attr.ib(init=True)
    @_commands.validator
    def validate_history(self, attribute, value):
        if type(value) != list:
            raise ValueError(f"Expected a list, instead a {type(value).__name__} was given")
        if not all(type(x) == Command for x in value):
            raise ValueError(f"Expected all list elements to be instances of Command")

    def execute(self) -> None:
        for c in self._commands:
            c.execute()


@attr.s
class BaseTransformDatasetCommand(Command):
    dataset = attr.ib(init=True)
    feature = attr.ib(init=True)

    def execute(self) -> None:
        raise NotImplementedError


@attr.s
class TransformDatasetCommand(BaseTransformDatasetCommand):
    transformer = attr.ib(init=True)

    def execute(self) -> None:
        self.transformer(self.dataset, self.feature)


####### Commands
# @attr.s
# class RawExtractionCommand(TransformDatasetCommand):
#     transformer = attr.ib(init=False, default=attr.Factory(lambda self: self.feature.function, takes_self=True))
#
@attr.s
class AttributeAddDeleteCommand(Command, ABC):
    dataset = attr.ib(init=True)
    feature = attr.ib(init=True)
    state = attr.ib(init=True)

@attr.s
class AugmentDataCommnad(AttributeAddDeleteCommand):
    computer = attr.ib(init=True)

    def execute(self) -> None:
        values = self.computer(self.dataset, self.feature)
        self.feature.update(self.state.key, self.state.reporter)
        self.dataset.datapoints.observations[self.state.index] = values

    def get_undo(self):
        return UndoAddColumnCommnad(self.data_handler, self.dataset, self.feature, self.state)


class UndoAddColumnCommnad(AttributeAddDeleteCommand):
    def execute(self) -> None:
        if self.state.key == feature.current:
            raise RuntimeError(
                f"Requested to delete attribute/column '{self.state.key}', but it is the current state of feature {str(self.feature)}")
        del self.dataset.datapoints.observations[f'{feature.id}-{state.key}']
        del self.feature.states[state.key]

#############

@attr.s
class RawDiscretizeCommand(AugmentDataCommnad): pass

class EncodeCommand(AugmentDataCommnad):
    def execute(self) -> None:
        res = self.computer(self.dataset, self.feature)


@attr.s
class RemoveColumnCommand(Command):
    _receiver = attr.ib(init=True)
    dataset = attr.ib(init=True)
    feature = attr.ib(init=True)

    def execute(self) -> None:
        self._receiver.remove_column(dataset, feature)


@attr.s
class LoadDatapointsCommand(Command):
    datapoints_factory = attr.ib(init=True)
