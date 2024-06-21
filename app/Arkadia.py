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
                self.events_listen()
            except KeyboardInterrupt:
                self.log.write_and_print("Выполнено принудительное отключение бота")
                self.log.save_logs()
                break
            except Exception as err:
                self.log.only_print("Произошла непредвиденная ошибка! Проверьте логи!")
                self.log.only_write(err)
            finally:
                self.log.save_logs()

    def events_listen(self):
        from app.core.vk_used.vk_listener import VkListener
        from app.core.vk_used.vk_sender import VkSender
        listener = VkListener()
        sender = VkSender()
        listener.add_action_to_event(lambda event: sender.send_response(self.make_response(event)), VkEventType.MESSAGE_NEW)
        listener.add_action_to_event(lambda event: sender.send_response(self.make_response(event)), VkEventType.MESSAGE_EDIT)
        listener.start_listen()

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
    def has_correct_api(module) -> bool:
        return hasattr(module, "commands") and \
            hasattr(module, "assembly_message") and \
            hasattr(module, "has_commands")
