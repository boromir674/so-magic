import attr
import pandas as pd
from green_magic.strain.data.data_commands import CommandsManager
from ..backend import Backend
from green_magic.strain.data.dataset import Datapoints, DatapointsFactory

from green_magic.commands_manager import Command


class PDDatapointsFactory(DatapointsFactory):

    def from_json(self, file_path):
        raise NotImplementedError

    def from_json_lines(self, file_path, **kwargs):
        self.state = Datapoints(pd.read_json(file_path, lines=True))
        _id = 'filename'
        if 'id' in kwargs:
            _id = kwargs['id']
        super().from_json_lines(file_path, id=_id)


@attr.s
class PDCommandsManager(CommandsManager):
    prototypes = attr.ib(init=True, default=attr.Factory(lambda self: {
        'empty': Command(None, 'Null'),
        'json_line_dataset': Command(self.datapoints_factory, 'from_json_lines'),
    }, takes_self=True))


@attr.s
@Backend.register_as_subclass('pandas')
class PDBackend(Backend):
    handler = attr.ib(init=True, default=None)
    _commands_manager = attr.ib(init=False, default=PDCommandsManager(PDDatapointsFactory()))

    @property
    def commands(self):
        return self._commands_manager
