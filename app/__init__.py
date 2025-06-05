from time import sleep
from app import Logger


logger = Logger
global_cmd_prefix = "!!!"


def start(listener = None, cmd_prefix = None):
    from config import version, api
    from .tdn import check_connect
    global global_cmd_prefix
    ok = False
    if api is not None:
        while not ok:
            try:
                ok, response = check_connect()
                if not ok:
                    raise Exception(f"Can not connect to server: {response}")
            except Exception as e:
                logger.write_and_print(e)
                sleep(1)
    else:
        print("Bot is running without connection to server")

    if cmd_prefix is None:
        cmd_prefix = "/"
    global_cmd_prefix = cmd_prefix
    if listener is None:
        from app.Arkadia import Arkadia
        listener = Arkadia(version, cmd_prefix)
    listener.start()

