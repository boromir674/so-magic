import attr


@attr.s
class DatapointsTransformer:
    _datapoints = attr.ib(init=True)
    transformer = attr.ib(init=True)

    def transform(self, **kwargs):
        return self.transformer.transform(self._datapoints, **kwargs)
