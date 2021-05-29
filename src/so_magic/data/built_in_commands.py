"""Defines functions that will serve as engine commands with an arbitrary object as receiver.
These commands should be "built" using a suitable function/decorator.
At runtime, their (command) arguments are the same as the function holding the business logic.
"""
from so_magic.data.features.phis import ListOfCategoricalPhi, DatapointsAttributePhi


# at runtime it will expect only the 'datapoints', 'attribute' and 'new_attribute' arguments
def encode_nominal_subsets_command(datapoints, attribute, new_attribute):
    phi = ListOfCategoricalPhi(DatapointsAttributePhi(datapoints))
    new_values = phi(attribute)
    datapoints.mutator.add_column(datapoints, new_values, new_attribute)
