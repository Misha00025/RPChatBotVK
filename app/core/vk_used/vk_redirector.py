from datetime import datetime

from .vk_sender import VkSender
from vk_api.longpoll import Event
from app.core import alias_managent as am
from app.core.base_interface.Response import Response


_redirect = "--redirect--"
_service = "--service--"


def _generate_message(event: Event):
    owner_id = str(event.user_id)
    sender_name = am.get_alias(owner_id)
    if event.from_me:
        sender_name = "ГМ"
    message = f"{_redirect}\nОт: {sender_name}:\n{event.text}"
    return message


_redirected_messages = {}
_last_clear = datetime


class VkRedirector:

    def __init__(self, sender, logger):
        self.sender: VkSender = sender
        self.log = logger

    @staticmethod
    def remember_message(event: Event):
        print("Remember message")
        red_msg: RedirectedMessage
        if not event.from_me:
            return
        for key in _redirected_messages:
            red_msg = _redirected_messages[key]
            if str(event.user_id) in red_msg.users and red_msg.text == event.text:
                red_msg.messages_for_users.append((event.message_id, event.user_id))

    def redirect_message(self, event: Event):
        from app.core import locations
        if event.from_chat: 
            return
        message_owner = str(event.user_id)
        location = locations.get_user_location(message_owner)
        users: list = locations.get_users(location)
        if users is None:
            return
        users.remove(message_owner)
        message = _generate_message(event)
        response = Response(message, users)
        message_id = str(event.message_id)
        _redirected_messages[message_id] = RedirectedMessage(users, message)
        self.sender.send_response(response)

    def edit_redirected_messages(self, event: Event):
        message_id = str(event.message_id)
        if not message_id in _redirected_messages.keys():
            return
        rm: RedirectedMessage = _redirected_messages[message_id]
        users = rm.messages_for_users
        message = _generate_message(event)
        print(f"{users};\n{message}")
        response = Response(message, users)
        self.sender.edit_message(response)


class RedirectedMessage:
    def __init__(self, users, text):
        self.users = users
        self.text = text
        self.messages_for_users = []

