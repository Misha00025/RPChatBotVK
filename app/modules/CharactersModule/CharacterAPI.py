from .CharacterFromDB import CharacterFromDB
from ..BaseModule.BaseAPI import BaseAPI
from .CommandExecuter import CommandExecuter
from app.UserFromDB import UserFromDB


class CharacterAPI(BaseAPI):

    def __init__(self):
        self.character_from_db = CharacterFromDB()

        self.executer = CommandExecuter()
        self.commands = ["персонаж"]
        super().__init__(self.commands)

    def assembly_message(self, user: UserFromDB, command_lines) -> str:
        message = ""

        for line in command_lines:
            message += self.executer.execute_command(user, line)
        return message


