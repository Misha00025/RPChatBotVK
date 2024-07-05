import json


class TdnSession:
    def __init__(self, service_token):
        import requests
        self._rq = requests
        self._api_version = "v1"
        self._url = f"http://127.0.0.1:5000/api/{self._api_version}/"
        self._headers = {"Service-token": service_token, "Content-Type": "application/json"}

    def _get_param(self, command, args):
        url = self._url + command
        if args is None:
            args = {}
        return url, args

    def get(self, command: str, args: dict = None):
        url, args = self._get_param(command, args)
        return self._rq.get(url, params=args, headers=self._headers)

    def post(self, command: str, data: dict):
        url, args = self._get_param(command, None)
        return self._rq.post(url, json=data, headers=self._headers)

    def put(self, command: str, data: dict, args: dict = None):
        url, args = self._get_param(command, args)
        return self._rq.put(url, params=args, json=data, headers=self._headers)


_session: TdnSession = None


def get_session() -> TdnSession:
    global _session
    if _session is None:
        from config import service_token
        _session = TdnSession(service_token)
    return _session


from . import api
