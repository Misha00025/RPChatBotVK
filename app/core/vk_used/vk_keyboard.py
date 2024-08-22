from vk_api.longpoll import Event
from .vk_connector import get_connector
from vk_api.keyboard import VkKeyboard as VkK
from vk_api.keyboard import VkKeyboardColor
from vk_api.utils import get_random_id
from config import keyboard_file as file_path


class VkKeyboard:
    def __init__(self):
        self._connector = get_connector()

    def _generate_keyboard(self):
        keyboard = VkK(one_time=True)  # Создаем экземпляр клавиатуры
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                text = line.strip()  # Убираем лишние пробелы и переносы строк
                if text == "nl":
                    keyboard.add_line()  # Добавляем новую строку
                else:
                    keyboard.add_button(text, color=VkKeyboardColor.SECONDARY)  # Добавляем кнопку
        self._keyboard = keyboard

    def get_keyboard(self):
        self._generate_keyboard()
        return self._keyboard.get_keyboard()

    def send(self, event: Event):
        if event.text != "/keyboard":
            return
        api = self._connector.get_api()
        api.messages.send(
            user_id=event.user_id,
            message="Клавиатура отправлена",
            random_id=get_random_id(),
            keyboard=self.get_keyboard()
        )

