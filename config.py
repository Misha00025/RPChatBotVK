import configparser


_conf = configparser.ConfigParser()
_conf.read("config.ini")


version = _conf["DEFAULT"]["Version"]
log_file_name = _conf["DEFAULT"]["LogFIle"]
token_file_name = _conf["DEFAULT"]["TokenFIle"]
db_connection_file_name = _conf["DEFAULT"]["DbConnectionSettingsFile"]

try:
    _db_config = configparser.ConfigParser()
    _db_config.read(db_connection_file_name)
    connection_settings = _db_config["DATABASE"]
except:
    print(f"File \"{db_connection_file_name}\" do not exist!")
    connection_settings = None

# create a file "token.txt" and insert your vk token into it
token = open(token_file_name, "r", encoding="utf-8").read()
