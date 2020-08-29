import attr
from .features import AttributeReporter


@attr.s
class DatapointsAttributePhi:
    datapoints = attr.ib(init=True)

    def _extract(self, attribute):
        return self.datapoints.column(attribute)


def _values_set(list_to_nominal):
    if str(list_to_nominal.attribute_reporter) not in list_to_nominal.datapoints_attribute_phi.datapoints.get_categorical_attributes():
        raise RuntimeError(f"Requested to use the 'list_to_nominal' encoder, but the given variable '{str(list_to_nominal.attribute_reporter)}',"
                           f"seems to not belong in the categorical variables of the structured data (so can't be nominal as well).")
    return list_to_nominal.attribute_reporter.values_set(list_to_nominal.datapoints_attribute_phi.datapoints)


@attr.s
class ListOfCategoricalPhi:
    datapoints_attribute_phi = attr.ib(init=True)
    attribute_reporter = attr.ib(init=False, default=None)
    _set = attr.ib(init=False, default=set())
    _ordering = attr.ib(init=False, default=list())
    _binary_transformer = attr.ib(init=False, default={True: 1, False: 0})

    @property
    def attribute(self):
        return str(self.attribute_reporter)

    @attribute.setter
    def attribute(self, attribute):
        self.attribute_reporter = AttributeReporter(attribute)
        self._set = _values_set(self)
        self._ordering = list(ListOfCategoricalPhi._order(self._set))

    def __call__(self, *args, **kwargs):
        """
        Args:
            attribute (str): the attribute we wish to target for input to the phi function
        """
        self.attribute_reporter = args[0]
        return iter([self._binary_transformer[x in datapoint] for x in self._ordering] for datapoint in self.datapoints_attribute_phi.datapoints.iterrows())

    @staticmethod
    def _order(x):
        return iter(_ for _ in sorted(x))
