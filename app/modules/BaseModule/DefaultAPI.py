from app.DataBase.User import User

from app.core.CommandParser import CommandParser
from .BaseAPI import BaseAPI


class DefaultAPI(BaseAPI):

    def __init__(self):
        self.commands = ["start", "помощь"]
        super().__init__(self.commands)

    def assembly_message(self, user: User, command_lines: [str], request: str) -> str:
        for cm in command_lines:
            if self.cp.find_command_in_line(cm) == self.commands[0]:
                from app.tdn.api import get_tdn_api
                api = get_tdn_api()
                print(api.add_user_to_me(user.get_user_id(), user.is_admin()))
                message = "--service--\n"
                message += "Здравствуйте.\nМеня зовут Аркадия.\nЯ -- бот-помощник для проведения текстовых ролевых игр."
                message += "\nПриятно с Вами познакомиться.\n"
                message += "Вот что я умею:\n"
                message += "1. Бросать кости. Для этого воспользуйтейсь командой: /к<N> или /d<N>, где N -- это количество граней бросаемой кости\n"
                message += "2. Сохранять заметки. Для этого воспользуйтесь командой: /заметки записать: <заголовок заметки>."
                message += " Обратите внимание, что весь текст сообщения после этой команды будет записан в заметку.\n"
                message += "3. Запоминать Ваши псевдонимы. Для этого воспользуйтесь командой: /псевдоним <новый псевдоним>\n"
                message += "4. Помещать Вас в зону к другим игрокам. Команда: /зона <название зоны>"
                return message
        message = "--service--\n"
        message += "Здравствуйте.\nМеня зовут Аркадия.\nЯ -- бот-помощник для проведения текстовых ролевых игр."
        message += "Вот что я умею:\n"
        message += "1. Бросать кости. Для этого воспользуйтейсь командой: /к<N> или /d<N>, где N -- это количество граней бросаемой кости\n"
        message += "2. Сохранять заметки. Для этого воспользуйтесь командой: /заметки записать: <заголовок заметки>."
        message += " Обратите внимание, что весь текст сообщения после этой команды будет записан в заметку.\n"
        message += "3. Запоминать Ваши псевдонимы. Для этого воспользуйтесь командой: /псевдоним <новый псевдоним>\n"
        message += "4. Помещать Вас в зону к другим игрокам. Команда: /зона <название зоны>"
        return message
