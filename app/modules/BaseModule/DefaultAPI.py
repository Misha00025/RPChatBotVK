from app.core.User import User

from .BaseAPI import BaseAPI


class DefaultAPI(BaseAPI):

    def __init__(self):
        self.commands = ["admin on", "admin off"]
        super().__init__(self.commands)

    def assembly_message(self, user: User, command_lines: [str], request: str) -> str:
        return "ok"

