from .vk_sender import VkSender
from .vk_connector import get_connector
from vk_api.longpoll import Event

from config import silence_prefix

from app.core.base_interface.Response import Response
from app.core.CommandParser import CommandParser
from app.core.MessageAssembler import get_assembler
from app.core import alias_managent as am


_silence = silence_prefix
_redirect = "--redirect--"
_service = "--service--"


class VkRouter:
    def __init__(self, sender: VkSender, logger):
        self.sender = sender
        self.log = logger
        self.assembler = get_assembler()
        self._connector = get_connector()

    def route_message(self, event):
        print("Поступило сообщение")
        if self.is_redirect(event) or self.is_service(event):
            return
        self.send_response(event)
        if not self.is_silence(event):
            self.redirect_message(event)

    def send_response(self, event):
        response: Response = self.make_response(event)
        message = response.message
        if message == "":
            return
        if self.is_silence(event):
            message = f"{_silence}\n{message}"
        response.message = message
        self.sender.send_response(response)

    def make_response(self, event: Event):
        group_id = self._connector.get_info().id
        admins = self._connector.get_info().admin_ids
        message = self.assembler.assembly_message(event, group_id, event.user_id in admins)
        response = Response(message, [event.user_id])
        if event.from_chat:
            response.set_chat_id(event.chat_id)
        return response

    def redirect_message(self, event: Event):
        from app.core import locations
        # print("Start redirect")
        message_owner = str(event.user_id)
        location = locations.get_user_location(message_owner)
        # print(location)
        users: list = locations.get_users(location)
        # print(users)
        if users is None:
            return
        users.remove(message_owner)
        sender_name = am.get_alias(message_owner)
        if event.from_me:
            sender_name = "ГМ"
        message = f"{_redirect}\nОт: {sender_name}:\n{event.text}"
        response = Response(message, users)
        self.sender.send_response(response)

    @staticmethod
    def is_silence(event):
        cp = CommandParser(commands=[""], prefix=_silence)
        cplen = len(cp.find_command_lines(event.message))
        return cplen != 0

    @staticmethod
    def is_redirect(event):
        cp = CommandParser(commands=[""], prefix=_redirect)
        cplen = len(cp.find_command_lines(event.message))
        return cplen != 0

    @staticmethod
    def is_service(event):
        cp = CommandParser(commands=[""], prefix=_service)
        cplen = len(cp.find_command_lines(event.message))
        return cplen != 0

