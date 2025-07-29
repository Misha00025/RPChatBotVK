from app.core.User import User
from app.modules.BaseModule.BaseAPI import BaseAPI
from app import model

def _add_note(user: User, params: tuple[str, str]) -> str:
    character = model.my_character(user)
    if character is None:
        return "Простите, но у вас пока нет персонажа"
    header, body = params
    ok = character.add_note(header, body)
    if ok:
        return "Запись успешно добавлена!"
    else:
        return "Не получилось добавить запись, обратитесь к админу :(\n"


def _get_notes(user: User, page: str = "") -> str:
    character = model.my_character(user)
    if character is None:
        return "Простите, но у вас пока нет персонажа"
    return "Я пока не умею показывать заметки"


def _del_note(user: User, note_id: str) -> str:
    character = model.my_character(user)
    if character is None:
        return "Простите, но у вас пока нет персонажа"
    return "Я пока не умею удалять заметки"


prefix = "заметки"


def find_note(line: str, request: str):
    tmp = request.split(line+'\n')
    if len(tmp) > 1:
        note = tmp[1]
    else:
        note = ""
    return note


class NotesAPI(BaseAPI):

    def __init__(self):
        self.commands = ["записать:", "удалить", "посмотреть"]
        for i in range(len(self.commands)):
            if self.commands[i] == "":
                self.commands[i] = prefix
                continue
            self.commands[i] = prefix + " " + self.commands[i]
        self._actions: dict = {
            self.commands[0]: lambda user, b: _add_note(user, b),
            self.commands[1]: lambda user, b: _del_note(user, b),
            self.commands[2]: lambda user, b: _get_notes(user, b),
        }
        super().__init__(self.commands)

    def assembly_message(self, user, command_lines: list[str], request) -> str:
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


