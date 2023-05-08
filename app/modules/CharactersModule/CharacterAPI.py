from .CharacterFromDB import CharacterFromDB
from ..BaseModule.BaseAPI import BaseAPI
from .CommandExecuter import CommandExecuter
from app.UserFromDB import UserFromDB


class CharacterAPI(BaseAPI):

    def __init__(self):
        self.executer = CommandExecuter()
        self.commands = ["персонаж"]
        super().__init__(self.commands)

    def assembly_message(self, user: UserFromDB, command_lines) -> str:
        message = ""

        for line in command_lines:
            command = self.cp.find_command_in_line(line)
            if command is None:
                continue
            parameters = self.cp.find_parameters_in_line(line, command)
            command_result = self.executer.execute_command(user, parameters)
            if command_result is None:
                continue
            message += command_result + "\n"
        if message == "":
            return None
        return message


