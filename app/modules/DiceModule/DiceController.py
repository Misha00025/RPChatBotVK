import random


decorators = [" &#128165;", " &#128128;"]


def redecorate(line: str) -> str:
    result = line
    for decorator in decorators:
        result = result.replace(decorator, "")
    return result


def _decorate_dice(result: int, dice) -> str:
    if result == 20 and int(dice) == 20:
        result = str(result) + decorators[0]
    elif result == 1 and int(dice) == 20:
        result = str(result) + decorators[1]
    return str(result)


def _get_first_num(string: str):
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

    def execute_command(self, command: str, parameters: str, prefix: str):
        '''
        :param command, parameters:
        :return message:
        '''
        # print(f"{prefix}{command}{parameters}")
        try:
            dice = _get_first_num(parameters)
            result_line = ""
            if prefix != "" and prefix.isalnum():
                results_dice = self.roll_dices(prefix, dice)
                results = ""
                for res in results_dice:
                    if results != "":
                        results += " + "
                    results += f"{_decorate_dice(res, dice)}"
                result_line = f"({results})"
            else:
                result_dice = self.roll_dice(dice)
                result_line = _decorate_dice(result_dice, dice)
            return result_line
        except:
            return None

    def is_correct_parameters(self, parameters: str) -> bool:
        return _get_first_num(parameters).isalnum()

    def roll_dices(self, count: str, parameters) -> list[int]:
        results = []
        for __ in range(int(count)):
            dice_result = self.roll_dice(parameters)
            results.append(dice_result)
        return results

    def roll_dice(self, dice) -> int:
        result = 1 + int(self._random.random() * int(dice))
        return result
