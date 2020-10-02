import pytest


@pytest.fixture
def command_interface():
    from so_magic.utils.commands import CommandInterface
    return CommandInterface


@pytest.fixture
def command_class():
    from so_magic.utils.commands import Command
    return Command


@pytest.fixture
def invoker():
    from so_magic.utils.commands import Invoker, CommandHistory
    return Invoker(CommandHistory())


def test_wrong_interface_usage(command_interface):
    class WrongChildClass(command_interface): pass
    with pytest.raises(TypeError) as e:
        a = WrongChildClass()
        assert "Can't instantiate abstract class WrongChildClass with abstract methods execute" == str(e)


def test_correct_command(command_class):
    def add(a_list, *args):
        return a_list.extend([_ for _ in args])

    input_list = [1]
    cmd = command_class(add, '__call__', input_list, 20, 100)
    cmd.execute()
    assert input_list == [1, 20, 100]
    cmd.append_arg(-1)
    cmd.execute()
    assert input_list == [1, 20, 100, 20, 100, -1]


def test_wrong_command(command_class):
    def add(a_list, *args):
        return a_list.gg([_ for _ in args])

    input_list = [1]
    cmd = command_class(add, '__call__', input_list, 22)
    with pytest.raises(AttributeError) as e:
        cmd.execute()
        assert "'list' object has no attribute 'gg'" == str(e)


def test_invoker(invoker, command_class):
    import copy
    class A:
        def b(self, x):
            res = x + 1
            print(res)
    a = A()

    cmd1 = command_class(a, 'b', 2)
    invoker.execute_command(cmd1)
    assert invoker.history.stack == []

    class A:
        def b(self, x):
            return x + 1

    a = A()
    cmd2 = copy.copy(cmd1)
    cmd2.args = [12]
    invoker.execute_command(cmd2)
    assert invoker.history.stack == []

    cmd3 = command_class(a, 'b', -1)
    invoker.execute_command(cmd3)
    assert invoker.history.stack == [cmd3]

    del cmd2
    invoker.execute_command(cmd1)
    assert invoker.history.stack == [cmd3]

    assert cmd3 == invoker.history.stack.pop()
