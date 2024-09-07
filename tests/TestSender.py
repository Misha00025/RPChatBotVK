from app.core.base_interface.Response import Response
from app.core.vk_used.vk_sender import VkSender


class TestSender(VkSender):
    def __init__(self):
        super().__init__()

    def send_response(self, response: Response):
        addressees, message = response.addressee, response.message.replace("\n\n", "")
        if response.is_chat_response:
            self._write_msg_to_chat(addressees[0], message)
        else:
            for addressee in addressees:
                self._write_msg(addressee, message)

    def edit_message(self, response: Response):
        # print("Edit messages in vk")
        addressees, message = response.addressee, response.message
        for addressee in addressees:
            message_id, user_id = addressee
            self._edit_message(user_id, message_id, message)

    def _edit_message(self, peer_id, message_id, new_message):
        print(f"Edit {message_id} from {peer_id} to: {new_message}")

    def _write_msg(self, user_id, message):
        print(f"Send to {user_id}: {message}")

    def _write_msg_to_chat(self, chat_id, message):
        print(f"Send to {chat_id}: {message}")
    