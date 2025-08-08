from typing import Callable
from app.core.User import User
from app.modules.BaseModule.BaseAPI import BaseAPI
from .ItemsProcessing import show_items, add_item, remove_item, set_item


PREFIX = "инвентарь"


class ItemsAPI(BaseAPI):

    def __init__(self):
        self.actions: dict[str, Callable[[User, str], str]]
        commands = {
            PREFIX+" добавить": add_item,
            PREFIX+" убрать": remove_item,
            PREFIX+" установить": set_item,
            PREFIX+"": show_items
        }
        super().__init__(commands)
    

    def assembly_message(self, user, command_lines: list[str], request) -> str:
        answer = ""
        i = 0
        for line in command_lines:
            command = self.cp.find_command_in_line(line)
            if command == "":
                continue
            i += 1
            params = self.cp.find_parameters_in_line(line)
            answer += self.actions[command](user, params) + "\n"
        if i > 1:
            answer += "\n--------------------------\n\n"+show_items(user, "")
        return answer
    
