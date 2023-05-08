from app.CommandParser import CommandParser
from app.UserFromDB import UserFromDB


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
        print(command)
        return self.events[command](user, command_line)

    def create_character(self, user: UserFromDB, command_line):
        parameters = self.cp.find_parameters_in_line(command_line)
        message = ""
        if parameters == "":
            return "Создать персонажа без имени нельзя"
        query = f"INSERT INTO public.\"character\"(owner_id, character_id, character_name) VALUES " \
                f"('{user.get_user_id()}', {self._get_last_character_id(user)+1}, '{parameters}');"
        try:
            self.db.execute(query)
            message = "Персонаж успешно создан"
        except Exception as err:
            message = err
        return message

    def get_character(self, user: UserFromDB, command_line):
        pass

    def _get_last_character_id(self, user) -> int:
        query = f"SELECT character_id FROM public.\"character\" WHERE owner_id = '{user.get_user_id()}';"
        res = self.db.fetchall(query)
        if len(res) == 0:
            return 0
        return int(res[len(res)-1][0])

