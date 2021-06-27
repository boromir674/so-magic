"""Defines functions that will serve as engine commands with an arbitrary object as receiver.
These commands should be "built" using a suitable function/decorator.
At runtime, their (command) arguments are the same as the function holding the business logic.
"""
from so_magic.data.features.phis import ListOfCategoricalPhi


# at runtime it will expect only the 'datapoints', 'attribute' and 'new_attribute' arguments
def encode_nominal_subsets_command(datapoints, attribute, new_attribute):
    phi = ListOfCategoricalPhi(datapoints)
    new_values = phi(attribute)
    nn = list(new_values)
    print('-------\n', nn, '\n-------\n')
    datapoints.mutator.add_column(datapoints, nn, new_attribute)
