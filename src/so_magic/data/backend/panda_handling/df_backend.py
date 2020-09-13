from so_magic.data.backend.engine_specs import EngineTabularRetriever, EngineTabularIterator, EngineTabularMutator
from so_magic.data.backend.engine import DataEngine
import pandas as pd

__all__ = ['PDTabularRetriever', 'PDTabularIterator', 'PDTabularMutator']


@EngineTabularRetriever.register_as_subclass('pd')
class PDTabularRetriever(EngineTabularRetriever):
    """The observation object is the same as the one your return from 'from_json_lines'"""
    def column(self, identifier, data):
        return data.observations[identifier]

    def row(self, identifier, data):
        return data.observations.loc(identifier)

    def nb_columns(self, data):
        return len(data.observations.columns)

    def nb_rows(self, data):
        return len(data.observations)

    def get_numerical_attributes(self, data):
        return data.observations._get_numeric_data().columns.values


@EngineTabularIterator.register_as_subclass('pd')
class PDTabularIterator(EngineTabularIterator):
    """The observation object is the same as the one your return from 'from_json_lines'"""

    def columnnames(self, data):
        return [_ for _ in data.observations.columns]

    def iterrows(self, data):
        return iter(data.observations.iterrows())

    def itercolumns(self, data):
        return iter(data.observations[column] for column in data.observations.columns)


@EngineTabularMutator.register_as_subclass('pd')
class PDTabularMutator(EngineTabularMutator):
    def add_column(self, datapoints, values, new_attribute, **kwargs):
        datapoints.observations[new_attribute] = values
