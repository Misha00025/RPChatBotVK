from vk_api.longpoll import Event

from .DiceController import DiceController, redecorate
from app.modules.BaseModule.BaseAPI import BaseAPI
from app.CommandParser import CommandParser


_math_simbols = ["+", "-", "/", "*", "(", ")"]
_simbols = ["(", ")"]


def parce_parameters(cp: CommandParser, line: str) -> (str, str):
    parameters = line
    next_line = ""
    return (parameters, next_line)




def parce_line_on_command(cp: CommandParser, line) -> (str, str, str):
    result = None
    command = cp.find_command_in_line(line)
    if command is None:
        return result
    
    prefix = cp.find_prefix_in_line(line, command)
    parameters = cp.find_parameters_in_line(line, command)

    return prefix, command, parameters


def parce_line_on_sublines(line: str) -> [str]:
    result = [line]
    for a in _math_simbols:
        parts = []
        for part in result:
            parts.extend(part.split(a))
        result = parts
    return result


def replace(source_line: str, old_and_new_list: list) -> str:
    result = ""
    if len(old_and_new_list) == 0:
        return source_line
    if source_line == "":
        return ""
    subline = old_and_new_list[0][0]
    result_subline = old_and_new_list[0][1]
    old_and_new_list.remove(old_and_new_list[0])
    index = source_line.find(subline)
    new_line = source_line[0 : index + len(subline)]
    new_line = new_line.replace(subline, result_subline)
    if subline != source_line:
        next_line = source_line[index + len(subline): ]
        new_line += replace(next_line, old_and_new_list)

    result = new_line
    return result



class DicesAPI(BaseAPI):

    def __init__(self):
        self.commands = ["dice ", "d", "куб ", "к"]
        super().__init__(self.commands)
        self.dice_controller = DiceController()

    def assembly_message(self, user, command_lines: [str]) -> str:
        import numexpr as ne
        message = ""
        for line in command_lines:                
            clean_line = str(line).replace(" ", "")
            sublines = parce_line_on_sublines(clean_line)
            sublines_with_results = []
            # print(sublines)
            for subline in sublines:
                commands = parce_line_on_command(self.cp, subline)
                if commands is None:
                    sublines_with_results.append((subline, subline))
                    continue
                prefix, command, parameters = commands
                if command in self.commands:
                    result = self.dice_controller.execute_command(command, parameters, prefix)
                    sublines_with_results.append((subline, result))
            try:
                formula = replace(line, sublines_with_results)
            except:
                return None
            clean_formula = redecorate(formula)
            message += f"Результат броска {line}: {ne.evaluate(clean_formula)} ({formula}) \n"
        return message