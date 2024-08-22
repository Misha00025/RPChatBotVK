import configparser
import os.path


def _conf_path(file_name):
    return os.path.join("configs", file_name)


_conf = configparser.ConfigParser()
_conf.read(_conf_path("config.ini"))


log_file_name = _conf["DEFAULT"]["LogFIle"]
st_file_name = _conf_path(_conf["DEFAULT"]["ServiceTokenFile"])
keyboard_file = _conf_path(_conf["DEFAULT"]["KeyboardFile"])
token_file_name = _conf_path(_conf["VK"]["TokenFile"])


version = open("version", "r", encoding="utf-8").read()
silence_prefix = _conf["DEFAULT"]["SilencePrefix"]
token = open(token_file_name, "r", encoding="utf-8").read()
service_token = str(open(st_file_name, "r", encoding="utf-8").readline()).strip()
