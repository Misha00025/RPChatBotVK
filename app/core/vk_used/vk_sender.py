from app.core.vk_used.vk_connector import get_connector
from app.core.base_interface.Response import Response
from vk_api.utils import get_random_id


class VkSender:
    def __init__(self):
        self._connector = get_connector()
        self._api = self._connector.get_api()

    def send_response(self, response: Response):
        addressees, message = response.addressee, response.message
        import html
        message = html.unescape(message)
        if response.is_chat_response:
            self._write_msg_to_chat(addressees[0], message)
        else:
            for addressee in addressees:
                self._write_msg(addressee, message)

    def _write_msg(self, user_id, message):
        if message == "":
            return
        self._api.messages.send(
            user_id=user_id,
            message=message,
            random_id=get_random_id()
        )

    def _write_msg_to_chat(self, chat_id, message):
        if message == "":
            return
        self._api.messages.send(
            chat_id=chat_id,
            message=message,
            random_id=get_random_id()
        )





