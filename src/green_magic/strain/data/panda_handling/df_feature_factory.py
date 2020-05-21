from ..variables import TrackingFeature, FeatureFactory


class DFFeatureFactory(FeatureFactory):
    def get_feature(self, column, **kwargs) -> TrackingFeature:
        return TrackingFeature.from_callable(lambda x: x[column], label=kwargs.get('label', column))
