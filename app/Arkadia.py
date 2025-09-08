from vk_api.longpoll import Event, VkEventType

import app
from app.core.vk_used.vk_keyboard import VkKeyboard
from app.core.vk_used.vk_router import VkRouter


class Arkadia:

    def __init__(self, version, cmd_prefix, debug=False):
        self.name = "Аркадия"

        self.log = app.logger
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

    def _get_listener_and_sender(self):
        from app.core.vk_used.vk_listener import VkListener
        from app.core.vk_used.vk_sender import VkSender
        return VkListener(), VkSender()
    
    def check_admin(self, event: Event):
        self.log.write_and_print("check admin")
        if not event.from_me:
            return
        from app.core.master_registry import append_masters, remove_masters
        from app.core.CommandParser import CommandParser
        from app import global_cmd_prefix
        self.log.only_print("check admin from me")
        parser = CommandParser(["admin on", "admin off"], global_cmd_prefix)
        request = event.text
        command_lines: list = parser.find_command_lines(request)
        if len(command_lines) > 1 or len(command_lines) == 0:
            return
        if (command_lines[0] == "admin on"):
            append_masters(event.user_id)
        elif (command_lines[0] == "admin off"):
            remove_masters(event.user_id)


    def _events_listen(self):
        listener, self.sender = self._get_listener_and_sender()
        self.keyboard = VkKeyboard()
        router = VkRouter(self.sender, self.log)

        listener.add_action_to_event(lambda event: self.check_admin(event), VkEventType.MESSAGE_NEW)
        listener.add_action_to_event(lambda event: router.send_response(event), VkEventType.MESSAGE_NEW)
        listener.add_action_to_event(lambda event: router.route_message(event), VkEventType.MESSAGE_NEW)
        listener.add_action_to_event(lambda event: router.edit_routed_message(event), VkEventType.MESSAGE_EDIT)
        # TODO: listener.add_action_to_event(lambda event: router.delete_message(event), VkEventType.MESSAGE_DELETE)
        listener.start_listen()

