import os
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

@attr.s
class DatapointsManager:
    datapoints_objects = attr.ib(init=True, default={})
    _state = attr.ib(init=False, default='')

    def update(self, *args, **kwargs):
        datapoints_object = args[0].state
        key = args[0].name
        if key in self.datapoints_objects:
            raise RuntimeError(f"Attempted to register a new Datapoints object at the existing key '{key}'.")
        self.datapoints_objects[key] = datapoints_object
        self._state = key

    @property
    def state(self):
        return self._state
    @property
    def datapoints(self):
        return self.datapoints_objects[self._state]

@attr.s
class DatapointsFactory:
    observers = attr.ib(init=True, default=[])
    state = attr.ib(init=False, default=None)
    name = attr.ib(init=False, default=None)


    def subscribe(self, *observers):
        self.observers.extend([_ for _ in observers])
        # for observer in observers:
        #     self.observers.append(observer)
    def unsubscribe(self, observer):
        self.observers.remove(observer)
    def notify(self, *args, **kwargs):
        """Notify all observers/listeners."""
        for observer in self.observers:
            observer.update(*args, **kwargs)

    def from_json(self, file_path):
        self.notify(self)

    def from_json_lines(self, file_path, **kwargs):
        if kwargs['id'] == 'filename':
            self.name = os.path.basename(file_path)
        else:
            self.name = kwargs['id']
        self.notify(self)
