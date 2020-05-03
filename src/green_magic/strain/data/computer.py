from abc import ABC, abstractmethod

class ComputerInterface(ABC):
    @abstractmethod
    def compute(self, *args, **kwargs):
        raise NotImplementedError


class AbstractComputer(ComputerInterface, ABC): pass

class AbstractTransformer(ComputerInterface, ABC):

    def compute(self, dataset, feature):
        raise NotImplementedError

class FeatureTransformer(AbstractTransformer):

    def compute(self, dataset, feature):
        pass

    def __call__(self, *args, **kwargs):
        return self.compute(args[0], args[1])


class EncoderInterface(ABC):
    @abstractmethod
    def encode(self, *args, **kwargs):
        raise NotImplementedError


class AbstractEncoder(EncoderInterface, ABC): pass

class AbstractFeatureEncoder(AbstractEncoder, ABC):
    def __call__(self, *args, **kwargs):
        return self.encode(*args, **kwargs)


class BaseFeatureEncoder(AbstractFeatureEncoder, ABC): pass

