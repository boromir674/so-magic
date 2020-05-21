

class FeatureManager:

    def check_features(self, dataset: Dataset, features: Sequence[Feature]):
        for f in features:
            if not f.var_type:
                f.var_type = VariableType(f)
            else:
                f.var_type.check(f)

    def encoded_features(self, dataset: Dataset) -> List[Feature]:
        for feature in dataset.features:
            if feature.state.current == 'endoded':
                yield feature

    def to_encode_feature(self, dataset):
        for feature in dataset.features:
            if feature.state.current != 'endoded':
                yield feature

