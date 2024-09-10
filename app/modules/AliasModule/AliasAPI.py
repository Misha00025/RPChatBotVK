from app.core import alias_management as am
from ..BaseModule.BaseAPI import BaseAPI
from app.core.User import User


class AliasAPI(BaseAPI):
    def __init__(self):
        self._commands = ["псевдоним"]
        super().__init__(self._commands)

    def assembly_message(self, user: User, command_lines: [str], request: str) -> str:
        user_id = user.get_user_id()
        last_alias = am.get_alias(user_id)
        cl = ""
        for line in command_lines:
            cmd = self.cp.find_command_in_line(line)
            if cmd != "":
                cl = line
                break
        if cl == "":
            return ""
        new_alias = self.cp.find_parameters_in_line(cl)
        am.set_alias(user_id, new_alias)
        return f"Псевдоним изменён с {last_alias} на {new_alias}"
