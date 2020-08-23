import pytest

from green_magic.data.backend import DataEngine


def test_engine_registration():
    from green_magic.data.backend import DataEngine
    from green_magic.data.backend.engine import EngineType
    assert type(DataEngine) == EngineType
    from green_magic.data.command_factories import CommandRegistrator

    # type(type(DataEngine))
    ATTRS = ('registry', '_commands', 'command')
    DataEngine.new('test_pd')
    assert 'test_pd' in DataEngine.subclasses
    assert type(DataEngine.test_pd) == type(DataEngine)
    assert all(hasattr(DataEngine.test_pd, x) for x in ATTRS)

    DataEngine.new('data_lib')
    assert 'data_lib' in DataEngine.subclasses
    assert type(DataEngine.data_lib) == type(DataEngine)
    assert all(hasattr(DataEngine.data_lib, x) for x in ATTRS)

    for x in ATTRS:
        print(getattr(DataEngine.test_pd, x), getattr(DataEngine.data_lib, x))
        assert id(getattr(DataEngine.test_pd, x)) != id(getattr(DataEngine.data_lib, x)) != id(DataEngine.registry)

    assert id(DataEngine.test_pd.datapoints_factory) == id(DataEngine.data_lib.datapoints_factory)

    assert len(DataEngine.test_pd.registry) == 0
    assert len(DataEngine.data_lib.registry) == 0


# def test_data_manager(test_json_data, data_manager, test_engine, datapoints):
#     import types
#     from green_magic.utils import Command
#     from green_magic.data.features.phi import PhiFunction
#     assert data_manager.backend.engine.__class__.datapoints_factory not in PhiFunction.subject._observers
#
#     assert len(datapoints) == test_json_data['nb_lines']
#     assert set(datapoints.attributes) == test_json_data['attributes']
#
#     @DataEngine.test_pd.dec()
#     def add_attribute(_datapoints, values, new_attribute):
#         _datapoints.observations[new_attribute] = values
#
#     assert type(DataEngine.test_pd) == type(DataEngine)
#     assert type(DataEngine.test_pd.registry) == dict
#     assert type(DataEngine.test_pd._commands) == dict
#     assert 'add_attribute' in DataEngine.test_pd.registry
#     assert 'add_attribute' in DataEngine.test_pd._commands
#     assert 'add_attribute' not in DataEngine.registry
#
#     assert type(DataEngine.test_pd._commands['add_attribute']) == Command
#
#     cmd = data_manager.command.add_attribute
#     assert type(cmd._receiver) == types.FunctionType
#     assert cmd._method == '__call__'
#     cmd.args = [datapoints, [_ for _ in range(1, len(datapoints) + 1)], 'test_attr']
#
#     from green_magic.utils.commands import Invoker, CommandHistory
#     inv = Invoker(CommandHistory())
#     inv.execute_command(cmd)
#
#     assert set(datapoints.attributes) == set(_ for _ in list(test_json_data['attributes']) + ['test_attr'])
#
#     @DataEngine.dec()
#     def list_to_encoded(_datapoints, values, new_attribute):
#         _datapoints.observations[new_attribute] = values
#
#     assert 'list_to_encoded' in DataEngine.registry
#     assert 'list_to_encoded' not in DataEngine.test_pd.registry
