from vk_api.longpoll import Event, VkEventType

import app
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

    def _events_listen(self):
        from app.core.vk_used.vk_listener import VkListener
        from app.core.vk_used.vk_sender import VkSender
        listener = VkListener()
        self.sender = VkSender()
        redirector = VkRouter(self.sender, self.log)
        listener.add_action_to_event(lambda event: redirector.route_message(event), VkEventType.MESSAGE_NEW)
        # listener.add_action_to_event(lambda event: self.send_response(event), VkEventType.MESSAGE_EDIT)
        listener.start_listen()

