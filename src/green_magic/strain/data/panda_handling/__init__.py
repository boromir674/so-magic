from .data_handler import DataFHandler

from ..receiver import Backend


@Backend.register_as_subclass('df')
class DFBackend(Backend):
    @property
    def features_factory(self):
        from .df_feature_factory import df_features_factory
        return df_features_factory
    @property
    def handler(self):
        from .data_handler import data_handler
        return data_handler

    @property
    def commands_manager(self):
        from .commands import commands_manager
        return commands_manager

    @property
    def computing(self):
        from .df_discretization import FeatureDiscretizerFactory, DFEncoderFactory
        dis_f = FeatureDiscretizerFactory()
        enc_f = DFEncoderFactory()
        x = object()
        x.discetizer_factory = dis_f
        x.encoder_factory = enc_f
        return x
