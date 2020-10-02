from data.variables import TrackingFeature, FeatureFactory

@FeatureFactory.register_as_subclass('pandas')
class DFFeatureFactory(FeatureFactory):
    def get_feature(self, column, **kwargs) -> TrackingFeature:
        return TrackingFeature.from_callable(lambda x: x[column], label=kwargs.get('label', column), variable_type=kwargs.get('variable_type', None))
