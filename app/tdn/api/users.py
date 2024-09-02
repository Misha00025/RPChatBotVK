from app.Logger import write_and_print as print
from app.tdn import TdnSession
from app.tdn.api import TdnApi


class FieldsNames:
    user_id = "user_id"
    is_admin = "is_admin"


_fm = FieldsNames


class TdnUserApi(TdnApi):
    def __init__(self, tdn: TdnSession):
        super().__init__(tdn)

    def get_user_info(self, user_id):
        res = self.session.get(f"users/{user_id}")
        if res.ok:
            response = res.json()
        else:
            response = res.text
        return res.ok, response

    def user_is_mine(self, user_id):
        res = self.session.get(f"users/{user_id}")
        return res.ok, res.text

    def add_user_to_me(self, user_id, is_admin):
        res = self.session.post("users/add", {_fm.user_id: str(user_id), _fm.is_admin: is_admin})
        return res.ok, res.text

    def delete_user(self, user_id):
        res = self.session.delete(f"users/{user_id}")
        return res.ok, res.text

_api: TdnUserApi = None


def get_users_api() -> TdnUserApi:
    global _api
    if _api is None:
        from app.tdn import get_session
        _api = TdnUserApi(get_session())
    return _api
