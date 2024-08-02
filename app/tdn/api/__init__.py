from .. import TdnSession


class TdnApi:
    def __init__(self, tdn: TdnSession):
        self._session = tdn

    @property
    def session(self):
        return self._session


_api: TdnApi = None


def get_tdn_api() -> TdnApi:
    global _api
    if _api is None:
        from app.tdn import get_session
        _api = TdnApi(get_session())
    return _api
