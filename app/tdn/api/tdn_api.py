from app.tdn import TdnSession

class TdnApi:
    def __init__(self, tdn: TdnSession):
        self._session = tdn

    @property
    def session(self):
        return self._session