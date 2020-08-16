from green_magic.data.interfaces import TabularRetriever, TabularIterator, TabularReporter


class PDTabularRetriever(TabularRetriever):
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

class PDTabularIterator(TabularIterator):
    """The observation object is the same as the one your return from 'from_json_lines'"""

    def columnnames(self, data):
        return [_ for _ in data.observations.columns]

    def iterrows(self, data):
        return iter(data.observations.iterrows())

    def itercolumns(self, data):
        return iter(data.observations[column] for column in data.observations.columns)

class PDTabularReporter(TabularReporter):
    def column_names(self, data):
        return data.observations.columns

