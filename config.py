import configparser
import os.path


def _get_full_path(filename):
    full_path = os.path.abspath(filename)
    return full_path

class ApiInfo:
    version: str = "v1"
    protocol: str = "http"
    host: str = "localhost"
    port: int = 5000
    verify: str | bool = False


def _conf_path(file_name):
    return os.path.join("configs", file_name)


_conf = configparser.ConfigParser()
_conf.read(_conf_path("config.ini"))


log_file_name = _conf["DEFAULT"]["LogFIle"]
keyboard_file = _conf_path(_conf["DEFAULT"]["KeyboardFile"])
token_file_name = _conf_path(_conf["VK"]["TokenFile"])

api: ApiInfo = None
st_file_name: str = None

if "API" in _conf.keys():
    api = ApiInfo()
    api.version = _conf["API"]["Version"]
    api.protocol = _conf["API"]["Protocol"]
    api.host = _conf["API"]["Host"]
    if "Port" in _conf["API"].keys():
        api.port = int(_conf["API"]["Port"])
    else:
        api.port = None
    if "SSLVerify" in _conf["API"].keys():
        api.verify = _get_full_path(_conf["API"]["SSLVerify"])
    st_file_name = _conf_path(_conf["API"]["ServiceTokenFile"])
    service_token = str(open(st_file_name, "r", encoding="utf-8").readline()).strip()

version = open("version", "r", encoding="utf-8").read()
silence_prefix = _conf["DEFAULT"]["SilencePrefix"]
token = open(token_file_name, "r", encoding="utf-8").read()