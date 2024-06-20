from config import token, version
from app import Logger
from app.DataBase import DataBase


logger = Logger
database = DataBase(logger)


def start(listener = None, cmd_prefix = None):
    if cmd_prefix is None:
        cmd_prefix = "/"
    if listener is None:
        from app.Arkadia import Arkadia
        listener = Arkadia(token, version, cmd_prefix)
    listener.start()

