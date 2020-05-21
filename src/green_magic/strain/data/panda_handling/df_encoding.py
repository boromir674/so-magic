



class NominalEncoder(BaseFeatureEncoder):
    def encode(self, *args, **kwargs):
        dataset, feature = args[0], args[1]
        return pd.get_dummies(dataset.datapoints.observations.df, f'{feature.id}-{feature.current}')


class DFEncoderFactory:
    def get_encoder(self, feature):
        if feature.variable_type == '':
            return NominalEncoder()
        return ''
