

class Response:
    def __init__(self,
                 message: str,
                 addressee: list,
                 chat_id: str = None):
        self.message: str = message
        self.addressee: list = addressee
        self.is_chat_response = chat_id is not None
        if self.is_chat_response:
            self.addressee = [chat_id]

    def set_chat_id(self, chat_id):
        self.is_chat_response = chat_id is not None
        self.addressee = [chat_id]

