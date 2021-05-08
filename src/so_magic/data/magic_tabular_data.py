# from typing import Iterable
# import attr

# from .datapoints import AbstractTabularData, DatapointsFactory


# @attr.s
# # @DatapointsFactory.register_constructor('tabular-data')
# class TabularData(AbstractTabularData):
#     """Table-like datapoints that are loaded in memory"""

#     retriever = attr.ib(init=True)
#     iterator = attr.ib(init=True)
#     mutator = attr.ib(init=True)

#     @property
#     def columns(self) -> Iterable:
#         return self.iterator.columnnames(self)

#     @property
#     def rows(self) -> Iterable:
#         raise NotImplementedError

#     @property
#     def attributes(self):
#         return self.iterator.columnnames(self)

#     def column(self, identifier):
#         return self.retriever.column(identifier, self)

#     def row(self, identifier):
#         return self.retriever.row(identifier, self)

#     @property
#     def nb_columns(self):
#         return self.retriever.nb_columns(self)

#     @property
#     def nb_rows(self):
#         return self.retriever.nb_rows(self)

#     def iterrows(self):
#         return self.iterator.iterrows(self)

#     def itercolumns(self):
#         return self.iterator.itercolumns(self)

#     # TODO remove and use MagicData
#     def get_numerical_attributes(self):
#         return self.retriever.get_numerical_attributes(self)

#     # TODO remove and use MagicData
#     def get_categorical_attributes(self):
#         return iter(set(self.attributes) - set([_ for _ in self.retriever.get_numerical_attributes(self)]))


# # class MagicData(TabularData):
# #     @property
# #     def rows(self):
# #         raise NotImplementedError

# #     def get_numerical_attributes(self):
# #         return self.retriever.get_numerical_attributes(self)

# #     def get_categorical_attributes(self):
# #         return iter(set(self.attributes) - set([_ for _ in self.retriever.get_numerical_attributes(self)]))
