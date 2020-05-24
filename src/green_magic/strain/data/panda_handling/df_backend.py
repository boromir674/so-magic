import copy
import attr
import pandas as pd
from ..backend import Backend
from green_magic.strain.data.dataset import Datapoints, DatapointsFactory
from ..types import *

from strain.data.data_commands import Command


class PDDatapointsFactory(DatapointsFactory):

    def from_json(self, file_path):
        raise NotImplementedError

    def from_json_lines(self, file_path):
        return Datapoints(pd.read_json(file_path, lines=True))


@attr.s
class PDCommandsManager:
    prototypes = attr.ib(init=True, default={
        'read_json': Command(PDDatapointsFactory, 'from_json_lines')
    })

    def __getattr__(self, item):
        return copy.copy(self.prototypes[item])


@attr.s
@Backend.register_as_subclass('pandas')
class PDBackend(Backend):
    handler = attr.ib(init=True, default=None)
    _commands_manager = attr.ib(init=False, default=PDCommandsManager)

    @property
    def commands(self):
        return self._commands_manager

    @property
    @abc.abstractmethod
    def computing(self):
        raise NotImplementedError
