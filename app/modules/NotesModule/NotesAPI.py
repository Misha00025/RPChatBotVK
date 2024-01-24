from app.UserFromDB import UserFromDB
from app.modules.BaseModule.BaseAPI import BaseAPI
from app import database


def _add_note(user: UserFromDB, note: str) -> str:
    return ""


def _get_notes(user: UserFromDB, page: str = "") -> str:
    return ""


def _del_note(user: UserFromDB, note_id: str) -> str:
    return ""


prefix = "заметки"


class NotesAPI(BaseAPI):

    def __init__(self):
        self.commands = ["", "записать:", "удалить"]
        for i in range(len(self.commands)):
            if self.commands[i] == "":
                self.commands[i] = prefix
                continue
            self.commands[i] = prefix + " " + self.commands[i]
        self._actions: {} = {
            self.commands[0]: lambda user, b: _get_notes(user, b),
            self.commands[1]: lambda user, b: _add_note(user, b),
            self.commands[2]: lambda user, b: _del_note(user, b)
        }
        super().__init__(self.commands)

    def assembly_message(self, user, command_lines: [str]) -> str:
        answer = ""
        for line in command_lines:
            command = self.cp.find_command_in_line(line)
            parameters = self.cp.find_parameters_in_line(line, command)
            if command in self._actions.keys():
                answer += self._actions[command](user, parameters)
            else:
                answer += "Команда не распознана"
        return answer


