"""This module is responsible to define functions that will serve as engine commands with a DataManager instance as receiver.
These commands should be "built" using a suitable function/decorator.
At runtime, their (command) arguments are the same as the function holding the business logic, minus the first argument which should be a DataManager instance
that is "handled" internally.
"""

# at runtime it will expect only the 'variables' argument
def select_variables_command(_data_manager, variables):
    _data_manager.feature_manager.feature_configuration = variables
