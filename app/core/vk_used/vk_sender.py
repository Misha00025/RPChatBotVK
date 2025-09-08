from app.core.vk_used.vk_connector import get_connector
from app.core.base_interface.Response import Response
from vk_api.utils import get_random_id


class VkSender:
    def __init__(self):
        self._connector = get_connector()
        self._api = self._connector.get_api()

    def send_response(self, response: Response):
        addressees, message, attachments = response.addressee, response.message, response.attachments
        if response.is_chat_response:
            self._write_msg_to_chat(addressees[0], message)
        else:
            for addressee in addressees:
                self._write_msg(addressee, message, attachments)

    def edit_message(self, response: Response):
        # print("Edit messages in vk")
        addressees, message, attachments = response.addressee, response.message,response.attachments
        for addressee in addressees:
            message_id, user_id = addressee
            self._edit_message(user_id, message_id, message, attachments)

    def _edit_message(self, peer_id, message_id, new_message, attachments = None):
        if attachments is not None:
            self._api.messages.edit(
                peer_id=peer_id,
                message_id=message_id,
                message=new_message,
                attachment = attachments,
                dont_parse_links=1
            )
        else:
            self._api.messages.edit(
                peer_id=peer_id,
                message_id=message_id,
                message=new_message,
                dont_parse_links=1
            )

    def _write_msg(self, user_id, message, attachment = None):
        if message == "":
            return
        if attachment is not None:
            self._api.messages.send(
                user_id=user_id,
                message=message,
                random_id=get_random_id(),
                attachment = attachment
            )
        else:
            self._api.messages.send(
                user_id=user_id,
                message=message,
                random_id=get_random_id()
            )

    def _write_msg_to_chat(self, chat_id, message, attachment = None):
        if message == "":
            return
        if attachment is not None:
            self._api.messages.send(
                chat_id=chat_id,
                message=message,
                random_id=get_random_id(),
                attachment = attachment
            )
        else:
                self._api.messages.send(
                chat_id=chat_id,
                message=message,
                random_id=get_random_id(),
            )





