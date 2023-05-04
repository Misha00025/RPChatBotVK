import configparser


_conf = configparser.ConfigParser()
_conf.read("config.ini")

version = _conf["DEFAULT"]["Version"]

# create a file "token.txt" and insert your vk token into it
with open("token.txt", "r", encoding="utf-8") as f:
    token = f.read()