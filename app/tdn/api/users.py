from app.Logger import write_and_print as print
from app.tdn import TdnSession
from app.tdn.api import TdnApi


class FieldsNames:
    user_id = "user_id"
    status = "status"
    is_admin = "is_admin"


_fm = FieldsNames


class TdnUserApi(TdnApi):
    def __init__(self, tdn: TdnSession):
        super().__init__(tdn)

    def get_user_info(self, user_id):
        return self.session.get(f"get_user_info/{user_id}")

    def user_is_mine(self, user_id):
        res = self.session.get("user_is_mine", args={_fm.user_id: str(user_id)})
        if not res.ok:
            return False
        return res[_fm.status]

    def add_user_to_me(self, user_id, is_admin):
        res = self.session.post("add_user_to_me", {_fm.user_id: str(user_id), _fm.is_admin: is_admin})
        print(res.text)
        return res.ok


_api: TdnUserApi


def get_users_api() -> TdnUserApi:
    global _api
    if _api is None:
        from app.tdn import get_session
        _api = TdnUserApi(get_session())
    return _api
