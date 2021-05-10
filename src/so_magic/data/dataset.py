import attr


@attr.s(str=True, repr=True)
class Dataset:
    """High level representation of data, of some form.

    Instances of this class encapsulate observations in the form of datapoints
    as well as their respective feature vectors. Feature vectors can then be
    trivially "fed" into a Machine Learning algorithm (eg SOM).

    Args:
        datapoints ():
        name (str, optional):
    Returns:
        [type]: [description]
    """
    datapoints = attr.ib(init=True)
    name = attr.ib(init=True, default=None)

    _features = attr.ib(init=True, default=[])
    size = attr.ib(init=False, default=attr.Factory(lambda self: len(self.datapoints) if self.datapoints else 0,
                                                    takes_self=True))

    @property
    def features(self):
        return self._features

    @features.setter
    def features(self, features):
        self._features = features
