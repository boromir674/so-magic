from abc import ABC, abstractmethod

from collections import Counter
import attr


class CountsComputerInterface(ABC):
    @abstractmethod
    def compute_counts(self, *args, **kwargs):
        raise NotImplementedError

class AbstractCountsComputer(CountsComputerInterface, ABC):
    def __call__(self, *args, **kwargs):
        return self.compute_counts(*args, **kwargs)


@attr.s
class BaseCountsComputer(AbstractCountsComputer):

    def compute_counts(self, *args, **kwargs):
        return Counter(args[0])


# @attr.s
# class DatapointsCountsComputer(AbstractCountsComputer):
#     counts_computer = attr.ib(init=True)
#
#     def compute_counts(self, datapoints, attributes):
#         return {attrib: self.counts_computer(self._iter(datapoints, attrib)) for attrib in attributes}
#
#     def _iter(self, datapoints, k):
#         return iter(self._extract(d, k) for d in datapoints)
#
#     def _extract(self, datapoint, attribute):
#         return getattr(datapoint, attribute)


@attr.s
class ClusterCountsComputer(AbstractCountsComputer):
    datapoints_counts_computer = attr.ib(init=True)
    extractor = attr.ib(init=True)

    def compute_counts(self, cluster, attributes):
        return self.datapoints_counts_computer(self.extractor(cluster), attributes)

######################

class DistroComputerInterface(ABC):
    @abstractmethod
    def compute_frequencies(self, *args, **kwargs):
        raise NotImplementedError

class AbstractDistroComputer(DistroComputerInterface, ABC):
    def __call__(self, *args, **kwargs):
        return self.compute_frequencies(*args, **kwargs)


@attr.s
class BaseDistroComputer(AbstractDistroComputer):
    counts_computer = attr.ib(init=True)
    norm = attr.ib(init=False, default=None)

    def compute_frequencies(self, *args, **kwargs):
        _ = self.counts_computer(*args, **kwargs)
        self.norm = sum(_.values())
        return _ / self.norm


@attr.s
class DatapointsDistroComputer(AbstractDistroComputer):
    distro_computer = attr.ib(init=True)
    extractor = attr.ib(init=True)

    def compute_frequencies(self, datapoints, attributes):
        return {attrib: self.distro_computer(self.extractor(datapoints, attrib)) for attrib in attributes}


@attr.s
class ClusterDistroComputer(AbstractDistroComputer):
    datapoints_distro_computer = attr.ib(init=True)
    extractor = attr.ib(init=True)

    def compute_frequencies(self, cluster, attributes):
        return self.datapoints_distro_computer(self.extractor(cluster), attributes)

    @classmethod
    def from_extractors(cls, extractor1, extractor2):
        """Extractor 1 (cluster) -> datapoints, Extractor 2 (datapoints, attribute)"""
        return ClusterDistroComputer(DatapointsDistroComputer(BaseDistroComputer(BaseCountsComputer()), extractor2), extractor1)
