import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


def write_msg(user_id, message):
    vk.rand_id += 1
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': vk.rand_id})


class MyVkApi(vk_api.VkApi):

    rand_id = random.Random(1000).random()

    pass

while True:
    try:
        # API-ключ созданный ранее
        token = "vk1.a.WLLCmf8Gvp6Yql--XKPmQN7FueBQRPzFECykO7JyxQptcpPM1Tj7RfKHdLKr4iLEEIaJ5fqIWdH8Ijpf9kpu3I2iWJMiS1DXEqKI_LvaCeKBSB6FPNjiNVPS8_hVKUChR-7oWgdBX-1qRuFjfrVCaBch8Lbdno_zdV1aqgQEC7FGbmDgJr4225qfrftRBq_c2ogDRYtYiDDoGYWK49YpFA"

        # Авторизуемся как сообщество
        vk = MyVkApi(token=token)

        # Работа с сообщениями
        longpoll = VkLongPoll(vk)

        print("Подключение прошло успешно!")

        for event in longpoll.listen():

            # Если пришло новое сообщение
            if event.type == VkEventType.MESSAGE_NEW:
                print("take event")
                # Если оно имеет метку для меня( то есть бота)
                if event.to_me:

                    # Сообщение от пользователя
                    request = event.text

                    # Каменная логика ответа
                    if request == "Привет":
                        message = 'Здравствуйте, меня зовут Амадия. Если хотите узнать меня лучше, отправьте команду "Расскажи о себе" и я поведаю Вам больше'
                        write_msg(event.user_id, message)
                    elif request == "Расскажи о себе":
                        message = 'Моё имя -- Амадия. Я -- бот-ассистент для текстовых ролевых игр в чатах. ' \
                                  'Я ещё нахожусь в разработке, поэтому знаю только эти команды: \n\n' \
                                  '1. Расскажи о себе \n\n ' \
                                  'Ещё меня научили здороваться и прощаться, и я рада этому! ' \
                                  'Хочу всегда учиться чему-то новому, чтобы становиться всё полезнее и полезнее!'
                        write_msg(event.user_id, message)
                    elif request == "Пока":
                        write_msg(event.user_id, "До свидания")
    except Exception:
        print("Переподключение")

