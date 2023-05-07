import configparser


_conf = configparser.ConfigParser()
_conf.read("config.ini")

version = _conf["DEFAULT"]["Version"]
log_file_name = _conf["DEFAULT"]["LogFIle"]
token_file_name = _conf["DEFAULT"]["TokenFIle"]
connection_settings = _conf["DATABASE"]

# create a file "token.txt" and insert your vk token into it
token = open(token_file_name, "r", encoding="utf-8").read()
