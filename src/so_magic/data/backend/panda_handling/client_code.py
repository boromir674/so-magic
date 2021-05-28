from so_magic.data.backend.engine_specs import EngineTabularRetriever, EngineTabularIterator, EngineTabularMutator


__all__ = ['PDTabularRetrieverDelegate', 'PDTabularIteratorDelegate', 'PDTabularMutatorDelegate']


# DELEGATES
# User defined (engine dependent implementations of tabular operations)

class PDTabularRetrieverDelegate(EngineTabularRetriever):
    """The observation object is the same as the one your return from 'from_json_lines'"""

    @classmethod
    def column(cls, identifier, data):
        return data.observations[identifier]

    @classmethod
    def row(cls, identifier, data):
        return data.observations.loc(identifier)

    @classmethod
    def nb_columns(cls, data):
        return len(data.observations.columns)

    @classmethod
    def nb_rows(cls, data):
        print('\n------ DEBUG NB ROWS PDTabularRetrieverDelegate DATA TYPE', type(data), ' ------\n')
        return len(data.observations)

    @classmethod
    def get_numerical_attributes(cls, data):
        return data.observations._get_numeric_data().columns.values


class PDTabularIteratorDelegate(EngineTabularIterator):
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


class PDTabularMutatorDelegate(EngineTabularMutator):

    @classmethod
    def add_column(cls, datapoints, values, new_attribute, **kwargs):
        datapoints.observations[new_attribute] = values
