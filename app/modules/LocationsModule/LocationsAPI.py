from ..BaseModule.BaseAPI import BaseAPI
from app.core.User import User
from app.core import alias_managent as am
from app.core import locations

class LocationsAPI(BaseAPI):
    def __init__(self):
        self._commands = ["локация", "зона", "location"]
        super().__init__(self._commands)

    def assembly_message(self, user: User, command_lines: [str], request: str) -> str:
        user_id = user.get_user_id()
        cl = ""
        for line in command_lines:
            command = self.cp.find_command_in_line(line)
            if command != "":
                cl = line
                break
        zone = self.cp.find_parameters_in_line(cl)
        if zone == "":
            return self.check_zone(user_id)
        if zone.lower() == "удалить":
            return self.remove_zone(user_id)
        locations.add_user(zone, user_id)
        user_id = am.get_alias(user_id)
        return f"Пользователь {user_id} добавлен в зону {zone}"

    @staticmethod
    def has_zone(user_id):
        zone = locations.get_user_location(user_id)
        return zone is not None

    def check_zone(self, user_id):
        if self.has_zone(user_id):
            zone = locations.get_user_location(user_id)
            user_id = am.get_alias(user_id)
            return f"Пользователь {user_id} находится в зоне {zone}"
        return "У пользователя нет зоны"

    def remove_zone(self, user_id):
        if self.has_zone(user_id):
            zone = locations.get_user_location(user_id)
            locations.remove_user(zone, user_id)
            user_id = am.get_alias(user_id)
            return f"Пользователь {user_id} был удалён из зоны {zone}"
        return "У пользователя нет зоны"