from . import df_operations as dfop
from green_magic.data.base_handling import BaseDataHandler


@BaseDataHandler.register_as_subclass('df-handler')
class DataFHandler(BaseDataHandler):

    def get_all_variables(self, *args, **kwargs):
        return args[0].columns

    def get_categorical_variables(self, *args, **kwargs):
        return dfop.categorical_feats(args[0])

    def get_numerical_variables(self, *args, **kwargs):
        return dfop.numerical_feats(args[0])

    def missing(self, df):
        return dfop.missing_values(df)

    def add_state(self, dataset, feature, computer, state, cache_prev=True, **kwargs):
        values = computer(dataset, feature)
        prev_state = feature.state
        feature.update(state.key, state.reporter)
        dataset.datapoints.observations[state.index] = values
        if not cache_prev:
            self.del_state(dataset, feature, prev_state)

    def del_state(self, dataset, feature, state, **kwargs):
        # DEBUG CODE
        if state.key == feature.current:
            raise RuntimeError(f"Requested to delete attribute/column '{state.key}', but it is the current state of feature {str(feature)}")
        del dataset.datapoints.observations.df[f'{feature.id}-{state.key}']
        del feature.states[state.key]


data_handler = DataFHandler()

