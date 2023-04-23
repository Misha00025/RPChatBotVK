import random
import numexpr as ne


def get_first_num(string: str):
    result = str()

    while string[0].isalnum():
        result += string[0]
        if len(string) <= 1:
            break
        string = string[1:]

    return result


class DiceController:

    def __init__(self):
        self._random = random.Random()

    def execute_command(self, command, parameters) -> str:
        '''
        :param command, parameters:
        :return message:
        '''
        if self.is_correct_parameters(parameters):
            dice = get_first_num(parameters)
            result_dice = self.roll_dice(dice)
            # print(f"dice{dice} = {result_dice}")
            # print(result_dice)
            if dice == parameters:
                return f"Результат броска {command}{parameters}: {result_dice}"
            else:
                formula = str(result_dice) + parameters[len(dice):]
                return f"Результат броска {command}{parameters}: {ne.evaluate(formula)} ({formula})"
        else:
            return "Не могу выполнить команду :("

    def is_correct_parameters(self, parameters: str) -> bool:
        #TODO: Сделать проверку символов + и -. Добавить проверку префикса

        return True #parameters.isalnum()

    def roll_dice(self, dice) -> int:
        result = 1 + int(self._random.random() * int(dice))
        if result == 20 and int(dice) == 20:
            result = str(result) + " &#128165;"
        elif result == 1 and int(dice) == 20:
            result = str(result) + " &#128128;"
        return result
