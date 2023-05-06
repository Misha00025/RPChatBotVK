import random
import sys

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.vk_api import VkApi

from app.CommandParser import CommandParser
from app.Loaders import load_modules, load_commands
from app.Logger import Logger


class Arkadia:

    def __init__(self, token, version, log_file):
        self.token = token
        self._init_vk_session()

        self.name = "Аркадия"
        self._modules = load_modules(Arkadia.has_correct_api)
        self._commands = load_commands(self._modules, self.has_correct_api)
        self.command_parcer = CommandParser(self._commands, "/")

        self.log = Logger()
        self.log.write_errors_in_file()
        self.log.write_datetime_in_console()
        self.log.write_and_print(f'Инициализация модуля "{self.name}" версии {version} завершена!')

    def _init_vk_session(self):
        self.vk_session = VkApi(token=self.token)
        self.vk = self.vk_session.get_api()

    def start(self):
        while True:
            try:
                self.events_listen()
            except vk_api.exceptions.ApiError as err:
                self.log.only_write(err)
                self.log.only_print("Переподключение")
                self._init_vk_session()
                self.log.only_print(f'Бот "{self.name}" успешно переподключился к серверам ВК')
            except KeyboardInterrupt:
                self.log.write_and_print("Выполнено отключение бота извне!")
                break

    def events_listen(self):
        longpoll = VkLongPoll(self.vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and not event.from_group:

                request = str(event.text).lower()
                command_lines: [(str, str)] = self.command_parcer.find_command_lines(request)
                message = self.assembly_message(command_lines)

                if event.from_chat:
                    self.write_msg_to_chat(event.chat_id, message)
                    print(f'Message in chat_{event.chat_id} from user_{event.user_id}: {request}')
                else:
                    self.write_msg(event.user_id, message)
                    print(f'Message from user_{event.user_id}: {request}')

    def assembly_message(self, command_lines: [str]):
        message = ""
        for module in self._modules:
            if self.has_correct_api(module) and module.has_commands(command_lines):
                message += module.assembly_message(command_lines) + "\n\n"
        return message

    def write_msg(self, user_id, message):
        if message == "":
            return
        self.vk.messages.send(
            user_id=user_id,
            message=message,
            random_id=get_random_id()
        )

    def write_msg_to_chat(self, chat_id, message):
        if message == "":
            return
        self.vk.messages.send(
            chat_id=chat_id,
            message=message,
            random_id=get_random_id()
        )

    @staticmethod
    def has_correct_api(module) -> bool:
        return hasattr(module, "commands") and \
            hasattr(module, "assembly_message") and \
            hasattr(module, "has_commands")
