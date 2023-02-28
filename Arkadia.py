import inspect
import os
import sys

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.vk_api import VkApi

from CommandParser import CommandParser
from DiceController import DiceController







class Arkadia():

    def __init__(self, token, test_mode=False):
        self.token = token
        # self.vk = vk_api.VkApi(token=self.token)
        self.vk_session = VkApi(token=self.token)
        self.vk = self.vk_session.get_api()

        self.name = "Аркадия"

        self._modules = self.load_modules("apis")

        self._commands = self.load_commands()

        if test_mode:
            self.name = "Тася"
            self.command_parcer = CommandParser(self._commands, "!")
        else:
            self.command_parcer = CommandParser(self._commands, "/")
        print(f'Инициализация модуля "{self.name}" завершена!')

    def load_modules(self, path):
        """
        Import all modules from the given directory
        """
        if path[-1:] != '/':
            path += '/'
        if not os.path.exists(path):
            raise OSError("Directory does not exist: %s" % path)
        modules = []
        for f in os.listdir(path):
            # Ignore anything that isn't a .py file
            if len(f) > 3 and f[-3:] == '.py':
                modname = f[:-3]
                modpath = path[:-1] + "." + f[:-3]
                # Import the module
                __import__(modpath, globals(), locals(), [f'{modname}'])
                for name, obj in inspect.getmembers(sys.modules[modpath]):
                    if inspect.isclass(obj) and name == modname:
                        modules.append(obj())
        return modules

    def load_commands(self) -> [str]:
        commands = []
        for module in self._modules:
            if self.is_api(module):
                commands += module.commands
        return commands

    def start(self):
        while True:
            try:
                self.events_listen()
            finally:
                print("Выполняется попытка переподключения")
                self.vk = vk_api.VkApi(token=self.token)
                print(f'Бот "{self.name}" успешно переподключился к серверам ВК')

    def events_listen(self):
        longpoll = VkLongPoll(self.vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and not event.from_group:
                request = str(event.text).lower()
                commands_with_parameters: [(str, str)] = self.command_parcer.find_commands(request)
                message = self.assembly_message(event, commands_with_parameters)
                if event.from_chat:
                    self.write_msg_to_chat(event.chat_id, message)
                    print(f'Message in chat_{event.chat_id} from user_{event.user_id}')
                else:
                    self.write_msg(event.user_id, message)
                    print(f'Message from user_{event.user_id}')

    def assembly_message(self, event, commands_with_parameters: [(str, str)]):
        message = ""
        for module in self._modules:
            if self.is_api(module) and module.has_commands(commands_with_parameters):
                message += module.assembly_message(event.user_id, commands_with_parameters) + "\n\n"
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

    def is_api(self, module) -> bool:
        return hasattr(module, "commands") and \
            hasattr(module, "assembly_message") and \
            hasattr(module, "has_commands")