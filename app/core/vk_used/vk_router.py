from .vk_sender import VkSender
from vk_api.longpoll import Event

from app.core.base_interface.Response import Response
from app.core.CommandParser import CommandParser
from app.core.MessageAssembler import get_assembler
from app.core import alias_managent as am


_silence = "--silence--"
_redirect = "--redirect--"


class VkRouter:
    def __init__(self, sender: VkSender, logger):
        self.sender = sender
        self.log = logger
        self.assembler = get_assembler()

    def route_message(self, event):
        print("Поступило сообщение")
        if self.is_redirect(event):
            return
        self.send_response(event)
        if not self.is_silence(event):
            self.redirect_message(event)

    def send_response(self, event):
        response: Response = self.make_response(event)
        message = response.message
        if self.is_silence(event):
            message = f"{_silence}\n{message}"
        response.message = message
        self.sender.send_response(response)

    def make_response(self, event: Event):
        message = self.assembler.assembly_message(event)
        response = Response(message, [event.user_id])
        if event.from_chat:
            response.set_chat_id(event.chat_id)
        return response

    def redirect_message(self, event: Event):
        from app.core import locations
        message_owner = str(event.user_id)
        users: list = locations.get_users(locations.get_user_location(message_owner))
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

