import pandas as pd
from data.encoding import EncoderFactory, AbstractEncoder


class NominalEncoder(AbstractEncoder):
    def encode(self, *args, **kwargs):
        dataset, feature = args[0], args[1]
        return pd.get_dummies(dataset.datapoints.observations.df, f'{feature.label}-{feature.state.current}')


@EncoderFactory.register_as_subclass('pandas')
class DFEncoderFactory(EncoderFactory):
    def nominal_encoder(self, feature, **kwargs):
        return NominalEncoder()
