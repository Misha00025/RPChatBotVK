from .CharacterFromDB import CharacterFromDB
from modules.BaseModule.BaseAPI import BaseAPI


class CharacterAPI(BaseAPI):
    #TODO: заставить команды выполнять нужные действия
    def __init__(self):
        self.character_from_db = CharacterFromDB()

        self.events = {}

        self.events["создать"] = self.create_user
        self.events["посмотреть"] = self.show_characters
        self.events["редактировать"] = self.void_command
        self.events["выбрать"] = self.void_command

        self.commands = list(self.events.keys())

    def assembly_message(self, event, command_lines: [(str, str)]) -> str:
        message = ""

        for command, parameters in command_lines:
            if command in self.commands:
                message += self.execute_command(event.user_id, command, parameters) + "\n"

        return message

    def execute_command(self, user_id, command, parameters):
        return self.events[command](user_id, parameters)

    def create_user(self, user_id, parameters):
        if parameters == "":
            return "Нельзя создать персонажа без имени"
        self.character_from_db.create_character(user_id, parameters)
        return f"Вы хотите создать персонажа с именем: {parameters}, но я ещё не готова выполнить это действие"

    def show_characters(self, user_id, parameters):
        if parameters == "":
            characters = self.character_from_db.get_characters(user_id)
            if not characters:
                return "У вас нет персонажей"
        return "Я не могу посмотреть персонажей, простите :'С"



# api = CharacterAPI()
#
# cwp = [("создать", "ГМ"), ("создать", ""), ("посмотреть", "")]
#
# message = api.assembly_message(1, cwp)
# print(message)

