import random


class DiceController():

    def __init__(self):

        self.commands = ["dice ", "d", "куб ", "к"]

        self._random = random.Random()

    def execute_command(self, command, parameters) -> str:
        '''
        :param command, parameters:
        :return message:
        '''
        if self.is_correct_parameters(parameters):
            return f"Результат броска {command}{parameters}: {self.roll_dice(parameters)}"
        else:
            return "Не могу выполнить команду :("

    def is_correct_parameters(self, parameters: str) -> bool:
        return parameters.isalnum()

    def roll_dice(self, parameters) -> int:
        result = 1 + int(self._random.random() * int(parameters))
        return result

