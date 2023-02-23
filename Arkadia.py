import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


class Arkadia():

    def __init__(self, token):
        self.token = token
        self.vk = vk_api.VkApi(token=self.token)

        self.name = "Аркадия"

        print(f'Инициализация модуля "{self.name}" завершена!')

    def start(self):
        while True:
            try:
                self.events_listen()
            except Exception:
                print("Переподключение")
                self.vk = vk_api.VkApi(token=self.token)
                print(f"{self.name} успешно переподключилась к серверам ВК")
    def events_listen(self):

        longpoll = VkLongPoll(self.vk)

        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                request = event.text
                if request == "Привет":
                    self.say_hello(event=event)
                elif request == "Расскажи о себе":
                    self.say_about_yourself(event=event)
                elif request == "Пока":
                    self.write_msg(event.user_id, "До свидания")

    def say_hello(self, event):
        message = f'Здравствуйте, меня зовут {self.name}. Если хотите узнать меня лучше, отправьте команду "Расскажи о себе" и я поведаю Вам больше'
        self.write_msg(event.user_id, message)

    def say_about_yourself(self, event):
        message = f'Моё имя -- {self.name}. Я -- бот-ассистент для текстовых ролевых игр в чатах. ' \
                  'Я ещё нахожусь в разработке, поэтому знаю только эти команды: \n\n' \
                  '1. Расскажи о себе \n\n ' \
                  'Ещё меня научили здороваться и прощаться, и я рада этому! ' \
                  'Хочу всегда учиться чему-то новому, чтобы становиться всё полезнее и полезнее!'
        self.write_msg(event.user_id, message)

    def write_msg(self, user_id, message):
        self.vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': (random.Random().random()*1000000)})