from so_magic.data.interfaces import TabularRetriever, TabularIterator, TabularMutator

__all__ = ['BACKEND']


# User defined (engine dependent implementations of tabular operations)

class PDTabularRetrieverDelegate(TabularRetriever):
    """The observation object is the same as the one your return from 'from_json_lines'"""

    @classmethod
    def column(cls, identifier, data):
        return data.observations[identifier]

    @classmethod
    def row(cls, identifier, data):
        return data.observations.iloc[[identifier]]

    @classmethod
    def nb_columns(cls, data):
        return len(data.observations.columns)

    @classmethod
    def nb_rows(cls, data):
        return len(data.observations)

    @classmethod
    def get_numerical_attributes(cls, data):
        return data.observations._get_numeric_data().columns.values


class PDTabularIteratorDelegate(TabularIterator):
    """The observation object is the same as the one your return from 'from_json_lines'"""

    @classmethod
    def columnnames(cls, data):
        return list(data.observations.columns)

    @classmethod
    def iterrows(cls, data):
        return iter(data.observations.iterrows())

    @classmethod
    def itercolumns(cls, data):
        return iter(data.observations[column] for column in data.observations.columns)


class PDTabularMutatorDelegate(TabularMutator):

    @classmethod
    def add_column(cls, datapoints, values, new_attribute, **kwargs):
        datapoints.observations[new_attribute] = values


BACKEND = {
    'backend_id': 'pd',
    'backend_name': 'pandas',
    'interfaces': [
        PDTabularRetrieverDelegate,
        PDTabularIteratorDelegate,
        PDTabularMutatorDelegate,
    ]
}
