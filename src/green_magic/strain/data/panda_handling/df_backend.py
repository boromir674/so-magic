from typing import AnyStr

import attr
import pandas as pd
from ..backend import Backend
from green_magic.strain.data.dataset import Datapoints, Dataset
from ..types import *


@attr.s
@Backend.register_as_subclass('df')
class Backend(Backend):

    @property
    def computer(self):
        return ''

    def observations_from_file(self, file_path: AnyStr) -> Datapoints:
        pass

    handler = attr.ib(init=True, default=None)

    def datapoints_from_file(self, file_path: AnyStr):
        return Datapoints(pd.read_json(file_path, convert_dates=True))

    @property
    @abc.abstractmethod
    def commands_manager(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def computing(self):
        raise NotImplementedError