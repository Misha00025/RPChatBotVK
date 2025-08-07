from requests import Response
from .tdn_api import TdnApi


class TdnCharacterItemsApi(TdnApi):
    def __init__(self, tdn, character_id):
        super().__init__(tdn)
        self._id = character_id

    def get(self):
        return self.session.get(f"/characters/{self._id}/items")

    def post(self, name, description, amount):
        return self.session.post(f"/characters/{self._id}/items", data={"name": name, "description": description, "amount": amount})
    
    def put(self, item_id, data):
        return self.session.put(f"/characters/{self._id}/items/{item_id}", data=data)
    
    def delete(self, item_id):
        return self.session.delete(f"/characters/{self._id}/items/{item_id}")


class TdnCharacterNotesApi(TdnApi):
    def __init__(self, tdn, character_id):
        super().__init__(tdn)
        self.character_id = character_id

    def post(self, header, body) -> Response:
        return self.session.post(f"/characters/{self.character_id}/notes", data={"header": header, "body": body})

    def get(self, note_id=None, page=None):
        if note_id is not None:
            return self.session.get(f"/characters/{self.character_id}/notes/{note_id}")
        if page is not None:
            return self.session.get(f"/characters/{self.character_id}/notes", args = {"page": int(page)})
        return self.session.get(f"/characters/{self.character_id}/notes")


class TdnCharacterApi(TdnApi):
    def __init__(self, session, character_id):
        super().__init__(session)
        self._id = character_id

    def items(self) -> TdnCharacterItemsApi:
        return TdnCharacterItemsApi(self.session, self._id)

    def notes(self) -> TdnCharacterNotesApi:
        return TdnCharacterNotesApi(self.session, self._id)
    
    def get(self):
        return self.session.get(f"/characters/{self._id}")