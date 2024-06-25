import configparser

_conf_path = "configs/"

_conf = configparser.ConfigParser()
_conf.read(_conf_path + "config.ini")


version = _conf["DEFAULT"]["Version"]
log_file_name = _conf["DEFAULT"]["LogFIle"]
silence_prefix = _conf["DEFAULT"]["SilencePrefix"]
token_file_name = _conf_path + _conf["VK"]["TokenFIle"]
db_connection_file_name = _conf_path + _conf["DATABASE"]["DbConnectionSettingsFile"]

try:
    _db_config = configparser.ConfigParser()
    _db_config.read(db_connection_file_name)
    connection_settings = _db_config["DATABASE"]
except:
    print(f"File \"{db_connection_file_name}\" do not exist!")
    connection_settings = None

# create a file "token.txt" and insert your vk token into it
token = open(token_file_name, "r", encoding="utf-8").read()
