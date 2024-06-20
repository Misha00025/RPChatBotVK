from app.DataBase.UserFromDB import UserFromDB

from app.core.CommandParser import CommandParser


class BaseAPI:

    def __init__(self, commands: [] = None):
        self.events = {}
        if commands is None:
            commands = []
        self.commands = commands
        self.cp = CommandParser(commands=self.commands)

    def assembly_message(self, user: UserFromDB, command_lines: [str], request: str) -> str:
        pass

    def has_commands(self, command_lines) -> bool:
        if len(command_lines) == 0:
            return False
        for line in command_lines:
            if self.cp.find_command_in_line(line) in self.commands:
                return True
        return False

    def void_command(self, user_id, parameters) -> str:
        return "Команда ничего не делает, увы :С"