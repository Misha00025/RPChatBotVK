from vk_api.longpoll import Event


class TEvent(Event):
    def __init__(self, raw):
        super().__init__(raw)

    def _parse_peer_id(self):
        if self.peer_id in ["-100", "-101"]:  # Сообщение от/для группы
            self.from_group = True
            self.group_id = self.peer_id
        else:  # Сообщение от/для пользователя
            self.from_user = True
            self.user_id = self.peer_id