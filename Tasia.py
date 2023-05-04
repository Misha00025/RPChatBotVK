from Arkadia import Arkadia
from CommandParser import CommandParser
from Loaders import load_modules, load_commands


class Tasia:

    def __init__(self, version):

        self.name = "Тася"

        self._modules = load_modules(Arkadia.has_correct_api)

        self._commands = load_commands(self._modules, Arkadia.has_correct_api)

        self.command_parser = CommandParser(self._commands, "")

        print(f'Инициализация модуля "{self.name}" версии {version} завершена!')

    def start(self):
        self.events_listen()

    def events_listen(self):
        while True:
            message = input("Введите команду: ")
            if message == "quit":
                break
            cwp = self.command_parser.find_command_in_line(message)
            print(self.assembly_message([cwp]))

    def assembly_message(self, commands_with_parameters: [(str, str)]):
        message = ""
        for module in self._modules:
            if Arkadia.has_correct_api(module) and module.has_commands(commands_with_parameters):
                message += module.assembly_message(None, commands_with_parameters)
        return message