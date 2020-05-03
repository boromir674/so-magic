import abc
from somoclu import Somoclu

from .cluster import Grouping, Cluster
from .kernel_determination import kernel_getter


class AbstractExtrinsicEvaluation(abc.ABC):
    @abc.abstractmethod
    def evaluate(self, clustering):
        pass


class ExtrinsincEvaluation(AbstractExtrinsicEvaluation):
    def evaluate(self, clustering):
        pass


class PropertySeparationEvaluation(ExtrinsincEvaluation):
    def __init__(self, a_property):
        self._pr = a_property
        self.kernel_getter = kernel_getter['top-id-unigrams']

    def __str__(self):
        return "'{}' property in-cluster dominance evaluation\nKernel getter: n top-id-unigrams".format(self._pr)

    def evaluate(self, clustering, kernel_size=5):
        """Returns a float in [0, 1]. 1 Indicates perfect 'type' separation and 0 worst"""
        assert isinstance(clustering, Clustering)
        assert self._pr in clustering.freqs
        scores = []
        for cl in clustering:
            activated_members = self.kernel_getter.determine_kernel(cl, size=kernel_size)
            kernel_group = clustering.factory.get_grouping(activated_members, clustering.active_variables)
            dominant = determine_dominant_value_name(cl, self._pr)
            score = judge_group_for_dominance(kernel_group, self._pr, dominant)
            scores.append(score)

        return sum(scores) / float(len(scores))


def determine_dominant_value_name(grouping, fproperty):
    return max(grouping.freqs[fproperty].items(), key=lambda x: x[1])[0]


def judge_group_for_dominance(grouping, fproperty, property_value, scale=(0, 1)):
    assert isinstance(grouping, Grouping)
    assert fproperty in ('type', )
    assert scale[0] < scale[1]
    score = 0
    for k, v in grouping.freqs[fproperty].items():
        if k == property_value:
            score += v
        else:
            score += 1 - v
    score = score / len(grouping.freqs[fproperty].items())
    return scale[0] + score * (scale[1] - scale[0])


def get_type_separation_eval():
    return PropertySeparationEvaluation('type')


if __name__ == '__main__':
    pass
