from .CharacterFromDB import CharacterFromDB
from ..BaseModule.BaseAPI import BaseAPI
from .CommandExecuter import CommandExecuter
from app.UserFromDB import UserFromDB


class CharacterAPI(BaseAPI):

    def __init__(self):
        self.character_from_db = CharacterFromDB()

        self.events = {}

        self.events["создать"] = self.void_command
        self.events["посмотреть"] = self.void_command
        self.events["редактировать"] = self.void_command
        self.events["выбрать"] = self.void_command

        self.executer = CommandExecuter(self.events.keys())
        self.commands = ["персонаж"]
        super().__init__(self.commands)

    def assembly_message(self, user: UserFromDB, command_lines) -> str:
        message = ""

        if not user.exist():
            user.create_user(user._user_id)

        for line in command_lines:
            message += self.execute_command(user, line)

        return message

    def execute_command(self, user, command_line):
        return "Still in development"

