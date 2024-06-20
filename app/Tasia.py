from app.Arkadia import Arkadia
from app.core.CommandParser import CommandParser
from app.core.Loaders import load_modules, load_commands

from app import logger
from app.DataBase.UserFromDB import UserFromDB


class Tasia (Arkadia):

    def __init__(self, version):

        self.name = "Тася"

        self.logger = logger
        self.logger.write_datetime_in_console()
        # self.logger.write_errors_in_file()

        self._modules = load_modules(Arkadia.has_correct_api)
        self._commands = load_commands(self._modules, Arkadia.has_correct_api)
        self.command_parser = CommandParser(self._commands, "")

        self.logger.write_and_print(f"Commands: {self._commands}")
        self.logger.write_and_print(f'Инициализация модуля "{self.name}" версии {version} завершена!')

    def start(self):
            try:
                self.events_listen()
            except KeyboardInterrupt:
                self.logger.write_and_print("Выполнено отключение бота извне!")
                # self.logger.save_logs()

    def events_listen(self):
        while True:
            message = input("Введите команду: ")
            if message == "quit":
                break
            command_lines = self.command_parser.find_command_lines(message)
            self.logger.only_write(f"Input commands: {command_lines}")
            self.logger.write_and_print(self.assembly_message(UserFromDB("test_user"), command_lines))

