import attr


@attr.s(str=True, repr=True)
class Dataset:
    datapoints = attr.ib(init=True)
    name = attr.ib(init=True, default=None)
    _features = attr.ib(init=True, default=[])

    handler = attr.ib(init=True, default=None)
    size = attr.ib(init=False, default=attr.Factory(lambda self: len(self.datapoints), takes_self=True))

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, features):
        self._features = features

    @classmethod
    def from_file(cls, file_path, name):
        return Dataset(Datapoints.from_file(file_path), name)


@attr.s
class Datapoints:
    observations = attr.ib(init=True)

    def __getitem__(self, item):
        return self.observations[item]

    def __iter__(self):
        return iter(self.observations)

    def __len__(self):
        return len(self.observations)

    @classmethod
    def from_file(cls, file_path):
        import pandas as pd
        return Datapoints(pd.read_json(file_path))


class DatapointsFactory:

    def from_json(self, file_path):
        raise NotImplementedError

    def from_json_lines(self, file_path):
        raise NotImplementedError

    def load(self, command):
        command = som_master.commands_manager.json_line_dataset
        command.append_arg(raw_datafile_path)
        som_master.load_dataset(command)