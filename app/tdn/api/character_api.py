from requests import Response
from .tdn_api import TdnApi


class TdnCharacterItemsApi(TdnApi):
    def __init__(self, tdn, character_id):
        super().__init__(tdn)
        self._id = character_id


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