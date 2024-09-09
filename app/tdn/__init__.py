import json

from requests import Response
import requests as rq

class TdnSession:
    def __init__(self, service_token, protocol, host, port = None, verify=False):
        self._api_version = "v1"
        self._verify = verify
        if port is not None:
            host += f":{port}"
        self._protocol = protocol
        self._url = f"{protocol}://{host}/api/"
        self._headers = {"Service-token": service_token, "Content-Type": "application/json; charset=utf-8"}

    @property
    def verify(self):
        return self._verify

    def _get_param(self, command, args, versioned = True):
        url = self._url 
        if versioned:
            url += f"{self._api_version}/"
        url += command
        if args is None:
            args = {}
        return url, args

    def get(self, command: str, args: dict = None, versioned = True) -> Response:
        url, args = self._get_param(command, args, versioned)
        # print(self.verify)
        return rq.get(url, params=args, headers=self._headers, verify=self.verify)

    def post(self, command: str, data: dict, args: dict = None, versioned = True) -> Response:
        url, args = self._get_param(command, args, versioned)
        return rq.post(url, json=data, headers=self._headers, params=args, verify=self.verify)

    def put(self, command: str, data: dict, args: dict = None, versioned = True) -> Response:
        url, args = self._get_param(command, args, versioned)
        return rq.put(url, params=args, json=data, headers=self._headers, verify=self.verify)

    def delete(self, command: str, args: dict = None, versioned = True) -> Response:
        url, args = self._get_param(command, args, versioned)
        return rq.delete(url, params=args, headers=self._headers, verify=self.verify)
    
    def check(self):
        response = ""
        ping = False
        access = False
        if self._protocol not in ["http", "https"]:
            return False, f"Unsupported protocol: '{self._protocol}'"
        try:
            ping = self.get("ping", versioned=True).ok
            access = self.get("check_access", versioned=False)
            if access.ok == False:
                response = "Not valid token"
            response = "Success!"
        except Exception as err:
            response = err        
        return (ping and access.ok), response


_session: TdnSession = None


def get_session() -> TdnSession:
    global _session
    if _session is None:
        from config import service_token
        from config import api
        _session = TdnSession(service_token, api.protocol, api.host, api.port, api.verify)
    return _session


def check_connect():
    session = get_session()
    return session.check()


from . import api
