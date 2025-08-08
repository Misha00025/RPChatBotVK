import re

from app.core.User import User
from .DiceController import DiceController, redecorate
from app.modules.BaseModule.BaseAPI import BaseAPI
from app.core.CommandParser import CommandParser


_math_symbols = ["+", "-", "/", "*", "(", ")"]
_symbols = ["(", ")"]


def parse_parameters(cp: CommandParser, line: str) -> tuple[str, str]:
    parameters = line
    next_line = ""
    return (parameters, next_line)




def parse_line_on_command(cp: CommandParser, line) -> tuple[str, str, str]:
    result = None
    command = cp.find_command_in_line(line)
    if command is None:
        return result
    
    prefix = cp.find_prefix_in_line(line, command)
    parameters = cp.find_parameters_in_line(line, command)

    return prefix, command, parameters


def parse_line_on_sublines(line: str) -> list[str]:
    result = [line]
    for a in _math_symbols:
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


def get_param_value(user: User, param: str):
    import config as c
    from app.core import character_owners as co
    from app.tdn.api import character as get_api
    if c.api is None:
        return 0
    character_id = co.as_character(user.get_user_id())
    api = get_api(character_id)
    res = api.get()
    if not res.ok:
        return 0
    character: dict = res.json()
    if "fields" not in character.keys():
        return 0
    fields: dict = character["fields"]
    if param not in fields.keys():
        return 0
    return int(fields.get(param).get("value", 0))


def apply_modifier(char_value):
    """Применяет формулу"""
    import math
    return math.floor((char_value - 10) / 2)


def process_characteristics(matches: list, clean_line: str, user):
    """
    Обрабатывает найденные характеристики, учитывая наличие модификатора ('!')
    """
    for match in matches:
        full_char_name = match.strip(':')
        modifier = False
        if full_char_name.startswith('!'):
            modifier = True
            char_name = full_char_name[1:]  # Имя характеристики без модификатора
        else:
            char_name = full_char_name
        raw_value = str(get_param_value(user, char_name))
        char_value = float(raw_value) if isinstance(raw_value, (float, int)) or raw_value.isdigit() else 0
        if modifier:
            char_value = apply_modifier(char_value)
        clean_line = clean_line.replace(match, str(char_value))
    return clean_line


class DicesAPI(BaseAPI):

    def __init__(self):
        self.commands = ["dice ", "d", "куб ", "к"]
        super().__init__(self.commands)
        self.dice_controller = DiceController()

    def assembly_message(self, user, command_lines: list[str], request) -> str:
        import numexpr as ne
        message = ""
        for line in command_lines:                
            clean_line = str(line).replace(" ", "")
            matches = re.findall(r':([^:]+):', clean_line)
            clean_line = process_characteristics(matches, clean_line, user)
            sublines = parse_line_on_sublines(clean_line)
            sublines_with_results = []
            # print(sublines)
            for subline in sublines:
                commands = parse_line_on_command(self.cp, subline)
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