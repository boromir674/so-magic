import attr
import pandas as pd
from ..backend import Backend
from green_magic.strain.data.dataset import Datapoints, Dataset
from ..types import *


@attr.s
@Backend.register_as_subclass('df')
class Backend(Backend):
    handler = attr.ib(init=True, default=None)

    def datapoints_from_file(self, file_path: AnyStr):
        return Datapoints(pd.read_json(file_path, convert_dates=True))

    @abc.abstractmethod
    def check_features(self, dataset: Dataset, features: Sequence[Feature]):
        for f in features:
            if not f.var_type:
                f.var_type = VariableType(f)
            else:
                var_type.check(f)

    @abc.abstractmethod
    def encodable_features(self, dataset: Dataset) -> List[Feature]:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def features_factory(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def commands_manager(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def computing(self):
        raise NotImplementedError