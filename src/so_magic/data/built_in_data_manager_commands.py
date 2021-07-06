"""Defines functions that will serve as engine commands with a DataManager instance as receiver.
These commands should be "built" using a suitable function/decorator.
At runtime, their (command) arguments are the same as the function holding the business logic, minus the first argument
which should be a DataManager instance.
"""


# at runtime it will expect only the 'variables' argument
def select_variables_command(data_manager, variables):
    data_manager.feature_manager.feature_configuration = variables


def encode_command(data_manager, attribute, scheme='auto'):
    encoder = data_manager.create('encoder', attribute, scheme=scheme)
    values = encoder.encode(data_manager.datapoints, attribute)
    column_names = encoder.get_feature_names()
    data_manager.datapoints.add_columns(values, column_names)


def replace_empty_command(data_manager, attribute, value=None):
    filler = data_manager.create('filler', attribute, value=value)
    values = filler.fill(data_manager.datapoints, inplace=True)
