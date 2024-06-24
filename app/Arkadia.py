from vk_api.longpoll import Event, VkEventType

import app
from app.core.CommandParser import CommandParser
from app.core.Loaders import load_modules, load_commands
from app.DataBase.UserFromDB import UserFromDB
from app.core.base_interface.Response import Response


class Arkadia:

    def __init__(self, version, cmd_prefix, debug=False):
        self.name = "Аркадия"
        self._modules = load_modules(self.has_correct_api)
        self._commands = load_commands(self._modules, self.has_correct_api)
        self.command_parcer = CommandParser(self._commands, cmd_prefix)

        self.log = app.logger
        # self.log.write_errors_in_file()
        self.log.write_datetime_in_console()
        self.log.write_and_print(f'Инициализация модуля "{self.name}" версии {version} завершена!')

    def start(self):
        while True:
            try:
                self._events_listen()
            except KeyboardInterrupt:
                self.log.write_and_print("Выполнено принудительное отключение бота")
                self.log.save_logs()
                break
            except Exception as err:
                self.log.only_print("Произошла непредвиденная ошибка! Проверьте логи!")
                self.log.only_write(f"{err.with_traceback(err.__traceback__)}")
            finally:
                self.log.save_logs()

    def _events_listen(self):
        from app.core.vk_used.vk_listener import VkListener
        from app.core.vk_used.vk_sender import VkSender
        listener = VkListener()
        self.sender = VkSender()
        listener.add_action_to_event(lambda event: self.send_response(event), VkEventType.MESSAGE_NEW)
        listener.add_action_to_event(lambda event: self.send_response(event), VkEventType.MESSAGE_EDIT)
        listener.add_action_to_event(lambda event: self._redirect_message(event), VkEventType.MESSAGE_NEW)
        listener.start_listen()

    def _redirect_message(self, event: Event):
        if self.is_silence(event):
            return
        from app.core import locations
        self.log.only_print("Запущена переадресация")
        message_owner = str(event.user_id)
        self.log.only_print(f"Отправитель: {message_owner}")
        users: list = locations.get_users(locations.get_user_location(message_owner))
        self.log.only_print(f"Users: {users}")
        if users is None:
            return
        users.remove(message_owner)
        sender_name = message_owner
        if event.from_me:
            sender_name = "ГМ"
        message = f"--redirect--\nОт: {sender_name}:\n{event.text}"
        response = Response(message, users)
        self.sender.send_response(response)

    def send_response(self, event):
        if self.is_silence(event):
            return
        self.sender.send_response(self.make_response(event))

    def make_response(self, event: Event):
        request = event.text
        command_lines: list = self.command_parcer.find_command_lines(request)
        user = UserFromDB(event.user_id)
        message = self.assembly_message(user, command_lines, request)
        response = Response(message, [event.user_id])
        if event.from_chat:
            response.set_chat_id(event.chat_id)
        return response

    def assembly_message(self, user: UserFromDB, command_lines: list, request):
        message = ""
        for module in self._modules:
            if self.has_correct_api(module) and module.has_commands(command_lines):
                module_message = module.assembly_message(user, command_lines, request)
                if module_message is None:
                    continue
                message += module_message + "\n\n"
        return message

    @staticmethod
    def is_silence(event):
        cp = CommandParser(commands=[""], prefix="--redirect--")
        cplen = len(cp.find_command_lines(event.message))
        return cplen != 0

    @staticmethod
    def has_correct_api(module) -> bool:
        return hasattr(module, "commands") and \
            hasattr(module, "assembly_message") and \
            hasattr(module, "has_commands")
