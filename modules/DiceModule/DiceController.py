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

    def execute_command(self, command: str, parameters: str, prefix: str) -> str:
        '''
        :param command, parameters:
        :return message:
        '''
        # print(f"{prefix}{command}{parameters}")
        if self.is_correct_parameters(parameters):
            dice = get_first_num(parameters)
            if prefix != "" and prefix.isalnum():
                result_dice = self.roll_dices(prefix, dice)
            else:
                result_dice = self.decorate(self.roll_dice(dice), dice)
            if dice == parameters:
                return f"Результат броска {prefix}{command}{parameters}: {result_dice}"
            else:
                formula = str(result_dice) + parameters[len(dice):]
                return f"Результат броска {prefix}{command}{parameters}: {ne.evaluate(formula)} ({formula})"
        else:
            return "Не могу выполнить команду :("

    def is_correct_parameters(self, parameters: str) -> bool:
        #TODO: Сделать проверку символов + и -. Добавить проверку префикса

        return True #parameters.isalnum()

    def roll_dices(self, count: str, parameters) -> str:
        dices_sum = self.roll_dice(parameters)
        dices_sum_str: str = "(" + str(dices_sum)
        for __ in range(int(count)-1):
            dice_result = self.roll_dice(parameters)
            dices_sum_str += ", " + self.decorate(dice_result, parameters)
            dices_sum += dice_result
        res = str(dices_sum) + " " + dices_sum_str + ")"
        return res

    def decorate(self, result: int, dice) -> str:
        if result == 20 and int(dice) == 20:
            result = str(result) + " &#128165;"
        elif result == 1 and int(dice) == 20:
            result = str(result) + " &#128128;"
        return str(result)

    def roll_dice(self, dice) -> int:
        result = 1 + int(self._random.random() * int(dice))
        return result
