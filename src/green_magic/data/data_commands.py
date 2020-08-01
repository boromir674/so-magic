from abc import ABC, abstractmethod
import copy
import attr

from green_magic.commands_manager import CommandsManager

from .dataset import DatapointsFactory


class DataCommandsmanager(CommandsManager):
    def __init__(self, prototypes):
        super().__init__(dict(prototypes, **{'read_json': Command(DatapointsFactory, 'from_json_lines')}))
