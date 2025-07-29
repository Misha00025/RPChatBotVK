from app.tdn import api


class Character:
    def __init__(self, character_id):
        self._id = character_id

    def add_note(self, header, body) -> bool:
        res = api.character(self._id).notes().post(header, body)
        return res.ok

    def add_item(self, name, description, amount) -> bool:
        pass

    def items(self):
        pass

    def notes(self):
        pass