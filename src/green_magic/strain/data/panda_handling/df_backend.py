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
        _id = 'filename'  # indicate to automatically assign an id inferred from the file name path
        if 'id' in kwargs:
            _id = kwargs['id']  # use user-provided id
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
#
# from green_magic.strain.data.data_attributes import DataAttribute, DataAttributeFactory
#
# class PDDataAttribute(DataAttribute):
#     def values(self, dataset):
#         return dataset[self.name]
#
#
# class PDDataAttributeFactory(DataAttributeFactory):
#     def from_dataset(self, dataset, attribute_name, sortable=True, ratio=True):
#         categorical = dataset.datapoints._get_numeric_data().columns.values
#         if attribute_name in categorical:
#             if sortable:
#                 return PDDataAttribute(attribute_name, self.types['ordinal'])
#             return PDDataAttribute(attribute_name, self.types['nominal'])
#         numerical = list(set(dataset.datapoints.columns) - set(categorical))
#         if attribute_name in numerical:
#             if ratio:
#                 return PDDataAttribute(attribute_name, self.types['ratio'])
#             return PDDataAttribute(attribute_name, self.types['interval'])
#         raise Exception(f"The '{attribute_name}' attribute was not found in the dataframe columns [{', '.join(str(_ for _ in dataset.datapoints.columns.values))}].")
