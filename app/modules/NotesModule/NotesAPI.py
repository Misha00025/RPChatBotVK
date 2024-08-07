from app.core.User import User
from app.modules.BaseModule.BaseAPI import BaseAPI
from app.tdn.api.notes import get_notes_api


def _add_note(user: User, params: (str, str)) -> str:
    api = get_notes_api()
    header, body = params
    if user.group_id is not None:
        user_id = user.get_user_id()
        api.add_note(user_id, header, body)
        return "Запись успешно добавлена!"
    return "Не получилось добавить запись, обратитесь к админу :(\n" \
           "(Если он спросит, назовите код ошибки: 2.1)"


def _get_notes(user: User, page: str = "") -> str:
    return ""


def _del_note(user: User, note_id: str) -> str:
    return ""


prefix = "заметки"


def find_note(line: str, request: str):
    note = request.split(line+'\n')[1]
    return note


class NotesAPI(BaseAPI):

    def __init__(self):
        self.commands = ["записать:", "удалить"]
        for i in range(len(self.commands)):
            if self.commands[i] == "":
                self.commands[i] = prefix
                continue
            self.commands[i] = prefix + " " + self.commands[i]
        self._actions: {} = {
            # self.commands[0]: lambda user, b: _get_notes(user, b),
            self.commands[0]: lambda user, b: _add_note(user, b),
            self.commands[1]: lambda user, b: _del_note(user, b)
        }
        super().__init__(self.commands)

    def assembly_message(self, user, command_lines: [str], request) -> str:
        answer = ""
        for line in command_lines:
            command = self.cp.find_command_in_line(line)
            if command == self.commands[0]:
                parameters = self.cp.find_parameters_in_line(line, command)
                header = parameters
                note = find_note(line, request)
                answer += self._actions[self.commands[0]](user, (header, note))
                continue
            if command in self._actions.keys():
                parameters = self.cp.find_parameters_in_line(line, command)
                answer += self._actions[command](user, parameters)
            else:
                answer += "Команда не распознана"
        return answer


