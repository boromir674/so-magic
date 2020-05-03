import abc


class KernelDeterminer(abc.ABC):

    @abc.abstractmethod
    def determine_kernel(self, cluster, size):
        raise NotImplementedError


class StrainIdUnigramsKernelDeterminer(KernelDeterminer):
    def __init__(self):
        pass

    def determine_kernel(self, cluster, size):
        """Returns a list of strain IDs; for example ['amnesia', 'silver-haze']"""
        top_unigram_ids = [x[0] for x in cluster.id_grams.most_common(size)]
        activated_ids = [idd for idd in cluster.gen_ids() if any(x in idd.split('-') for x in top_unigram_ids)]
        return activated_ids


strain_id_unigrams_kernel_determinator = StrainIdUnigramsKernelDeterminer()

kernel_getter = {
    'top-id-unigrams': strain_id_unigrams_kernel_determinator
}
