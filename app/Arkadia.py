import random
import sys
from time import sleep

import vk_api
from requests.exceptions import ReadTimeout, ConnectionError
from vk_api.longpoll import VkLongPoll, VkEventType, Event
from vk_api.utils import get_random_id
from vk_api.vk_api import VkApi, VkApiMethod

import app
from app.CommandParser import CommandParser
from app.Loaders import load_modules, load_commands
from app import logger
from app.UserFromDB import UserFromDB


class Arkadia:

    def __init__(self, token, version, log_file):
        self.token = token
        self._init_vk_session()
        self.name = "Аркадия"
        self._modules = load_modules(Arkadia.has_correct_api)
        self._commands = load_commands(self._modules, self.has_correct_api)
        self.command_parcer = CommandParser(self._commands, "/")

        self._load_group_info()

        self.log = logger
        self.log.write_errors_in_file()
        self.log.write_datetime_in_console()
        self.log.write_and_print(f'Инициализация модуля "{self.name}" версии {version} завершена!')

    def _init_vk_session(self):
        self.vk_session = VkApi(token=self.token)
        self.vk: VkApiMethod = self.vk_session.get_api()

    def _load_group_info(self):
        import requests
        data = f"v={self.vk_session.api_version}&access_token={self.token}&lang=0"
        res = requests.post('https://api.vk.com/method/groups.getById', data=data)
        json = res.json()["response"][0]
        # print(json)
        self.group_id = json["id"]
        self.group_name = json["name"]
        self._save_group()

    def _save_group(self):
        res = app.database.fetchone(f"SELECT * FROM vk_group WHERE vk_group_id = '{self.group_id}'")
        if res is None:
            app.database.execute(f"INSERT INTO vk_group(vk_group_id, group_name) "
                                 f"VALUES ('{self.group_id}', '{self.group_name}')")
        else:
            app.database.execute(f"UPDATE vk_group SET group_name='{self.group_name}' "
                                 f"WHERE vk_group_id='{self.group_id}'")

    def start(self):
        error = "First connect"
        while True:
            try:
                self._connect(error)
                self.log.only_print(f'Бот "{self.name}" успешно подключился к серверам ВК')
                self.events_listen()
            except ReadTimeout as err:
                self.log.only_print("Попытка переподключения")
                error = err
            except ConnectionError as err:
                sleep(60)
                self.log.only_print("Попытка переподключения")
                error = err
            except KeyboardInterrupt:
                self.log.write_and_print("Выполнено отключение бота извне!")
                self.log.save_logs()
                break
            except Exception as err:
                self.log.only_print("Произошла непредвиденная ошибка! Проверьте логи!")
                error = err

    def _connect(self, err):
        self.log.only_write(err)
        self.log.save_logs()
        self._init_vk_session()
        longpoll = VkLongPoll(self.vk_session)

    def events_listen(self):
        longpoll = VkLongPoll(self.vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and not event.from_group:

                request = event.text
                command_lines: [(str, str)] = self.command_parcer.find_command_lines(request)
                user = UserFromDB(event.user_id, self.group_id)
                message = self.assembly_message(user, command_lines, request)

                if event.from_chat:
                    self.write_msg_to_chat(event.chat_id, message)
                    self.log.write_and_print(f'Message in chat_{event.chat_id} from user_{event.user_id}: {request}')
                else:
                    self.write_msg(event.user_id, message)
                    self.log.write_and_print(f'Message from user_{event.user_id}: {request}')

    def assembly_message(self, user: UserFromDB, command_lines: [str], request):
        message = ""
        for module in self._modules:
            if self.has_correct_api(module) and module.has_commands(command_lines):
                module_message = module.assembly_message(user, command_lines, request)
                if module_message is None:
                    continue
                message += module_message + "\n\n"
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
