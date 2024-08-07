import configparser

_conf_path = "configs/"

_conf = configparser.ConfigParser()
_conf.read(_conf_path + "config.ini")


version = open("version", "r", encoding="utf-8").read()
log_file_name = _conf["DEFAULT"]["LogFIle"]
silence_prefix = _conf["DEFAULT"]["SilencePrefix"]
st_file_name = _conf_path+_conf["DEFAULT"]["ServiceTokenFile"]
token_file_name = _conf_path + _conf["VK"]["TokenFile"]


token = open(token_file_name, "r", encoding="utf-8").read()
service_token = str(open(st_file_name, "r", encoding="utf-8").readline()).strip()
