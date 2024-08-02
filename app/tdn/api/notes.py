from app.Logger import write_and_print as print
from app.tdn import TdnSession
from app.tdn.api import TdnApi


def _get_args(user_id):
    return {"user_id": user_id}


def _get_data(header, body):
    return {"header": header, "body": body}


class TdnNotesApi(TdnApi):
    def __init__(self, tdn: TdnSession):
        super().__init__(tdn)

    def get_notes(self, user_id):
        args = _get_args(user_id)
        return self.session.get("notes", args=args)

    def get_note(self, user_id, note_id):
        args = _get_args(user_id)
        return self.session.get(f"notes/{note_id}", args=args)

    def edit_note(self, user_id, note_id, header, body):
        args = _get_args(user_id)
        data = _get_data(header, body)
        return self.session.put(f"notes/{note_id}", args=args, data=data)

    def delete_note(self, user_id, note_id):
        args = _get_args(user_id)
        return self.session.delete(f"notes/{note_id}", args=args)

    def add_note(self, user_id, header, body):
        args = _get_args(user_id)
        data = _get_data(header, body)
        return self.session.post("notes/add", args=args, data=data)


_api: TdnNotesApi = None


def get_notes_api() -> TdnNotesApi:
    global _api
    if _api is None:
        from app.tdn import get_session
        _api = TdnNotesApi(get_session())
    return _api