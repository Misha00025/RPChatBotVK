from app.CommandParser import CommandParser
from app.UserFromDB import UserFromDB
from app.modules.CharactersModule.Character import Character
from app.modules.CharactersModule.CharacterFromDB import CharacterFromDB


class CommandExecuter:

    def __init__(self):
        from app import database
        self.db = database

        self.events = {}

        self.events["создать"] = lambda user, parameters: self.create_character(user, parameters)
        self.events["посмотреть"] = lambda user, parameters: self.get_character(user, parameters)
        self.events["редактировать"] = lambda user, parameters: "Don't work"
        self.events["выбрать"] = lambda user, parameters: "Don't work"

        self.cp = CommandParser(self.events.keys())

    def execute_command(self, user, command_line):
        command = self.cp.find_command_in_line(command_line)
        if command is None:
            return None
        return self.events[command](user, command_line)

    def create_character(self, user: UserFromDB, command_line):
        parameters = self.cp.find_parameters_in_line(command_line)
        message = ""
        if parameters == "":
            return "Создать персонажа без имени нельзя"

        try:
            character = Character(parameters)
            CharacterFromDB(user, character=character).save()
            message = "Персонаж успешно создан"
        except Exception as err:
            message = err
        return message

    def get_character(self, user: UserFromDB, command_line):
        parameters = self.cp.find_parameters_in_line(command_line)
        prefix = self.cp.find_prefix_in_line(command_line)
        if parameters in ["", "все", "all"] and prefix == "":
            return CharacterFromDB.get_all_characters(user)
        if prefix.isalnum():
            character_id = int(prefix)
        else:
            return CharacterFromDB.get_all_characters(user)
        character = CharacterFromDB(user, character_id).character
        return character.to_message()



