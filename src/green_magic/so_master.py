import attr


@attr.s
class SoMaster:
    _data_manager = attr.ib(init=True)
    _dataset_constructor = attr.ib(init=True)
    _magic_map_manager_constructor = attr.ib(init=True)

    _map_manager = attr.ib(init=False, default=attr.Factory(lambda self: self._magic_map_manager_constructor(self), takes_self=True))
    _last_path = attr.ib(init=False, default='')

    _datasets = attr.ib(init=False, default={})

    def load_data(self, file_path, id=''):
        cmd = self._data_manager.command.observations
        cmd.args = [file_path]
        cmd.execute()
        self._last_path = file_path
        return self._data_manager.backend.datapoints_manager.datapoints

    @property
    def map(self):
        return self._map_manager

    @property
    def datapoints(self):
        return self._data_manager.backend.datapoints_manager.datapoints

    @property
    def dataset(self):
        datapoints_id = id(self._data_manager.backend.datapoints_manager.datapoints)
        if datapoints_id not in self._datasets:
            self._datasets[datapoints_id] = self._dataset_constructor(
                self._data_manager.backend.datapoints_manager.datapoints,
                self._last_path,
            )
        return self._datasets[datapoints_id]

    @classmethod
    def create(cls, data_manager):
        from .som import MagicMapManager
        from .data.dataset import Dataset
        return SoMaster(data_manager, Dataset, MagicMapManager)
