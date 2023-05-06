import configparser


_conf = configparser.ConfigParser()
_conf.read("config.ini")

version = _conf["DEFAULT"]["Version"]
log_file_name = _conf["DEFAULT"]["LogFIle"]
token_file_name = _conf["DEFAULT"]["TokenFIle"]

# create a file "token.txt" and insert your vk token into it
with open(token_file_name, "r", encoding="utf-8") as f:
    token = f.read()