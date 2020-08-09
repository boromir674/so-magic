# import pandas as pd
#
# from green_magic.data.backend.engine import DataEngine
# from green_magic.data.interfaces import TabularRetriever, TabularIterator
#
#
# class PDTabularRetriever(TabularRetriever):
#     """The observation object is the same as the one your return from 'from_json_lines'"""
#     def column(self, identifier, data):
#         return data.observations[identifier]
#
#     def row(self, identifier, data):
#         return data.observations.loc(identifier)
#
#     def nb_columns(self, data):
#         return len(data.observations.columns)
#
#     def nb_rows(self, data):
#         return len(data.observations)
#
#
# class PDTabularIterator(TabularIterator):
#     """The observation object is the same as the one your return from 'from_json_lines'"""
#
#     def columnnames(self, data):
#         return [_ for _ in data.observations.columns]
#
#     def iterrows(self, data):
#         return iter(data.observations.iterrows())
#
#     def itercolumns(self, data):
#         return iter(data.observations[column] for column in data.observations.columns)
#
#
# @DataEngine.register_as_subclass('pd')
# class PDEngine(DataEngine): pass
#
#
# @PDEngine.observations()
# def tabular_data(file_path, **kwargs):
#     return pd.read_json(file_path, lines=True)
#
#
#
#

# from green_magic.strain.data.data_attributes import DataAttribute, DataAttributeFactory
#
# class PDDataAttribute(DataAttribute):
#     def values(self, dataset):
#         return dataset[self.name]
#
#
# class PDDataAttributeFactory(DataAttributeFactory):
#     def from_dataset(self, dataset, attribute_name, sortable=True, ratio=True):
#         categorical = dataset.datapoints._get_numeric_data().columns.values
#         if attribute_name in categorical:
#             if sortable:
#                 return PDDataAttribute(attribute_name, self.types['ordinal'])
#             return PDDataAttribute(attribute_name, self.types['nominal'])
#         numerical = list(set(dataset.datapoints.columns) - set(categorical))
#         if attribute_name in numerical:
#             if ratio:
#                 return PDDataAttribute(attribute_name, self.types['ratio'])
#             return PDDataAttribute(attribute_name, self.types['interval'])
#         raise Exception(f"The '{attribute_name}' attribute was not found in the dataframe columns [{', '.join(str(_ for _ in dataset.datapoints.columns.values))}].")

