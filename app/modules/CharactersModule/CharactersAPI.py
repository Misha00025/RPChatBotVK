from typing import Callable
from app.core.User import User
from app.modules.BaseModule.BaseAPI import BaseAPI
from app.core import alias_management as am
from app.core.character_owners import set_character


PREFIX = "персонаж"


def try_set_character(user: User, params):
    from app.tdn.api import character as get_api
    api = get_api(params)
    res = api.get()
    if res.ok:
        character = res.json()
        name = character["name"]
        set_character(user.get_user_id(), character["id"])
        return f"Персонаж по имени {name} назначен игроку {am.get_alias(user.get_user_id())}"
    return f"Не получилось назначить персонажа"


class CharacterAPI(BaseAPI):

    def __init__(self):
        self.actions: dict[str, Callable[[User, str], str]]
        commands = {
            PREFIX+" назначить": try_set_character
        }
        super().__init__(commands)
    

    def assembly_message(self, user, command_lines: list[str], request) -> str:
        answer = ""
        for line in command_lines:
            command = self.cp.find_command_in_line(line)
            if command == "":
                continue
            params = self.cp.find_parameters_in_line(line)
            answer += self.actions[command](user, params)
        return answer
    
