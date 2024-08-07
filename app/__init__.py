from config import version
from app import Logger


logger = Logger
global_cmd_prefix = "!!!"


def start(listener = None, cmd_prefix = None):
    global global_cmd_prefix
    if cmd_prefix is None:
        cmd_prefix = "/"
    global_cmd_prefix = cmd_prefix
    if listener is None:
        from app.Arkadia import Arkadia
        listener = Arkadia(version, cmd_prefix)
    listener.start()

