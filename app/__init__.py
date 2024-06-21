from config import version
from app import Logger
from app.DataBase.DataBase import DataBase


logger = Logger
database: DataBase = DataBase(logger)


def start(listener = None, cmd_prefix = None):
    if cmd_prefix is None:
        cmd_prefix = "/"
    if listener is None:
        from app.Arkadia import Arkadia
        listener = Arkadia(version, cmd_prefix)
    listener.start()

