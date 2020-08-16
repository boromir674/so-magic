import attr
from green_magic.data.encoding import Encoder
from .phi import PhiFunction
from .features import AttributeReporter

class DatapointsEncoder(Encoder):
    def encode(self, datapoints, attribute, **kwargs):
        pass

@attr.s
class DatapointsPhi:
    phi = attr.ib(init=True)
    datapoints = attr.ib(init=True)

    def __call__(self, **kwargs):
        return self.phi(self._datapoints, **kwargs)

def _values_set(list_to_nominal):
    if list_to_nominal.attribute not in list_to_nominal.phi.datapoints.get_categorical_attributes():
        raise RuntimeError(f"Requested to use the 'list_to_nominal' encoder, but the given variable '{list_to_nominal.attribute}',"
                           f"seems to not belong in the categorical variables of the structured data (so can't be nominal as well).")
    return list_to_nominal.attribute_reporter.values_set(list_to_nominal.phi.datapoints)


@attr.s
@Encoder.register_as_subclass('list-to-nominal')
class ListToNominal(Encoder):
    _datapoints = attr.ib(init=True)
    attribute_reporter = attr.ib(init=True, converter=AttributeReporter)
    phi = attr.ib(init=False, default=attr.Factory(lambda self: DatapointsPhi(PhiFunction(self.encode), self._datapoints), takes_self=True))
    _set = attr.ib(init=True, default=attr.Factory(lambda self: _values_set(self), takes_self=True))
    _ordering = attr.ib(init=False, default=attr.Factory(lambda self: list(ListToNominal._order(self._set)), takes_self=True), type=tuple)

    def encode(self, *args, **kwargs):
        tr = {True: 1, False: 0}
        return iter([tr[x in datapoint] for x in self._ordering] for datapoint in self._datapoints.iterrows())

    @property
    def order(self):
        return self._ordering

    @staticmethod
    def _order(x):
        return iter(_ for _ in sorted(x))

    @staticmethod
    def _phi(x):
        return DatapointsPhi()

    @property
    def attribute(self):
        return str(self.attribute_reporter)

    @attribute.setter
    def attribute(self, attribute):
        self.attribute_reporter = AttributeReporter(attribute)
        self._set = _values_set(self)
        self._ordering = list(ListToNominal._order(self._set))

    @property
    def value_set(self):
        return self._set