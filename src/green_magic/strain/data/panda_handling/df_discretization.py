import pandas as pd

from ..discretization import FeatureDiscretizer, BinnerInterface, FeatureDiscretizerFactory


class DFSameLengthBinning(BinnerInterface):
    def bin(self, values, nb_bins):
        return pd.cut(values, nb_bins)

class DFQBinning(BinnerInterface):
    def bin(self, values, nb_bins):
        return pd.qcut(values, nb_bins)

class BinContinuous(BinnerInterface):
    def bin(self, values, nb_bins):
        return pd.cut(values, nb_bins)


class DFDiscretizer(FeatureDiscretizer):
    pass


@attr.s
class DFDiscretizerFactory(FeatureDiscretizerFactory):

    @classmethod
    def categorical(cls, feature, quantisized=False):
        if quantisized:
            return DFDiscretizer(DFQBinning(), feature)
        return DFDiscretizer(DFSameLengthBinning(), feature)

    @classmethod
    def numerical(cls, feature):
        return DFDiscretizer(BinContinuous(), feature)


from green_magic.strain.data.computer import BaseFeatureEncoder


class NominalEncoder(BaseFeatureEncoder):
    def encode(self, *args, **kwargs):
        dataset, feature = args[0], args[1]
        return pd.get_dummies(dataset.datapoints.observations.df, f'{feature.id}-{feature.current}')


class DFEncoderFactory:
    def get_encoder(self, feature):
        if feature.variable_type == '':
            return NominalEncoder()
        return ''
