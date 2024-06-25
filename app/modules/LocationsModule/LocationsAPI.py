from ..BaseModule.BaseAPI import BaseAPI
from ...DataBase.UserFromDB import UserFromDB
from app.core import alias_managent as am


class LocationsAPI(BaseAPI):
    def __init__(self):
        self._commands = ["локация", "зона", "location"]
        super().__init__(self._commands)

    def assembly_message(self, user: UserFromDB, command_lines: [str], request: str) -> str:
        from app.core import locations
        user_id = user.get_user_id()
        cl = ""
        for line in command_lines:
            command = self.cp.find_command_in_line(line)
            if command != "":
                cl = line
                break
        zone = self.cp.find_parameters_in_line(cl)
        locations.add_user(zone, user_id)
        user_id = am.get_alias(user_id)
        return f"Пользователь {user_id} добавлен в зону {zone}"
