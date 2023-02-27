import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from CommandParser import CommandParser
from DiceController import DiceController


class Arkadia():

    def __init__(self, token, test_mode=False):
        self.token = token
        self.vk = vk_api.VkApi(token=self.token)

        self.name = "Аркадия"

        self._base_commands = ["привет", "помощь", "пока"]
        self._dice_controller = DiceController()

        self._commands = self._base_commands + self._dice_controller.commands

        if test_mode:
            self.name = "Тася"
            self.command_parcer = CommandParser(self._commands, "/")
        else:
            self.command_parcer = CommandParser(self._commands)
        print(f'Инициализация модуля "{self.name}" завершена!')

    def start(self):
        while True:
            try:
                self.events_listen()
            except:
                print("Переподключение")
                self.vk = vk_api.VkApi(token=self.token)
                print(f'Бот "{self.name}" успешно переподключился к серверам ВК')
        # self.events_listen()

    def events_listen(self):

        longpoll = VkLongPoll(self.vk)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and not event.from_group:

                request = str(event.text).lower()
                commands_with_parameters: [{str, str}] = self.command_parcer.find_commands(request)
                message = self.assembly_message_to_commands(event, commands_with_parameters)


                if hasattr(event, 'chat_id'):
                    self.write_msg_to_chat(event.chat_id, message)
                    print(f'ChatID: {event.chat_id}, UserID: {event.user_id}')
                else:
                    self.write_msg(event.user_id, message)
                    print(f'ChatID: {event.user_id}, UserID: {event.user_id}')



    def assembly_message_to_commands(self, event, commands_with_parameters: [(str, str)]):
        message = ""
        for command, parameters in commands_with_parameters:
            if command in self._dice_controller.commands:
                message += self._dice_controller.execute_command(command, parameters)
            elif command in self._base_commands:
                message += self.execute_base_command(command, parameters)
            message += "\n"
        return message

    def execute_base_command(self, command: str, parameters: str):
        if command == "привет":
            return self.say_hello()
        elif command == "расскажи о себе":
            return self.say_about_yourself()
        elif command == "пока":
            return "До свидания"

    def say_hello(self):
        return f'Здравствуйте, меня зовут {self.name}. Если хотите узнать меня лучше, отправьте команду "Расскажи о себе" и я поведаю Вам больше'

    def say_about_yourself(self):
        return f'Моё имя -- {self.name}. Я -- бот-ассистент для текстовых ролевых игр в чатах. ' \
                  'Я ещё нахожусь в разработке, поэтому знаю только эти команды: \n\n' \
                  '1. Расскажи о себе \n\n ' \
                  'Ещё меня научили здороваться и прощаться, и я рада этому! ' \
                  'Хочу всегда учиться чему-то новому, чтобы становиться всё полезнее и полезнее!'

    def write_msg(self, user_id, message):
        if message == "":
            return
        self.vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': (random.Random().random()*1000000)})

    def write_msg_to_chat(self, chat_id, message):
        if message == "":
            return
        self.vk.method('messages.send', {'chat_id': chat_id, 'message': message, 'random_id': (random.Random().random()*1000000)})