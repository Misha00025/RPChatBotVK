from typing import Callable
from app.core.User import User
from app.modules.BaseModule.BaseAPI import BaseAPI
from .ItemsProcessing import show_items, add_item, remove_item


PREFIX = "кошель"


class WalletAPI(BaseAPI):

    def __init__(self):
        self.actions: dict[str, Callable[[User, str], str]]
        commands = {
            PREFIX+" дать": add_item,
            PREFIX+" забрать": remove_item,
            PREFIX: show_items
        }
        super().__init__(commands)
    

    def assembly_message(self, user, command_lines: list[str], request) -> str:
        answer = ""
        for line in command_lines:
            command = self.cp.find_command_in_line(line)
            if command == "":
                continue
            params = self.cp.find_parameters_in_line(line)
            answer += self.actions[command](user, "деньги " + params)
        return answer
    
