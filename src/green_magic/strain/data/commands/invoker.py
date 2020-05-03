import attr
from .base_command import Command, CommandHistory

@attr.s
class Invoker:

    history = attr.ib(init=False, default=CommandHistory)

    def execute_command(self, command: Command):
        if command.execute():
            self.history.push(command)
