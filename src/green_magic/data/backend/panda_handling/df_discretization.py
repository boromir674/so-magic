from abc import ABC
import pandas as pd

from data.discretization import BaseBinner, BinnerFactory


class BasePDBinner(BaseBinner, ABC):

    @classmethod
    def register_as_subclass(cls, binner_type):
        def wrapper(subclass):
            cls.subclasses[binner_type] = subclass
            return subclass
        return wrapper

    @classmethod
    def create(cls, binner_type, *args, **kwargs):
        if binner_type not in cls.subclasses:
            raise ValueError('Bad "BinnerFactory Backend type" type \'{}\''.format(binner_type))
        return cls.subclasses[binner_type](*args, **kwargs)


@BaseDFBinner.register_as_subclass('same-length')
class DFSameLengthBinning(BasePDBinner):

    def bin(self, values, nb_bins):
        return pd.cut(values, nb_bins)

@BaseDFBinner.register_as_subclass('quantisized')
class DFQBinning(BasePDBinner):

    def bin(self, values, nb_bins):
        return pd.qcut(values, nb_bins)


@BinnerFactory.register_as_subclass('pandas')
class PDBinnerFactory(BinnerFactory):

    def equal_length_binner(self, *args, **kwargs) -> DFSameLengthBinning:
        return DFSameLengthBinning()

    def quantisized_binner(self, *args, **kwargs) -> DFQBinning:
        return DFQBinning()

    def create_binner(self, *args, **kwargs) -> BasePDBinner:
        BasePDBinner.create(*args, **kwargs)

