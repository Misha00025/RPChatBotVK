from app.core.DataSaver import load, save


SAVE_NAME = "masters"

_masters = set()



def get_masters():
    return _masters.copy()

def append_masters(user_id):
    _masters.append(str(user_id))
    save_masters()

def remove_masters(user_id):
    _masters.remove(str(user_id))
    save_masters()

def save_masters():
    save(_masters, SAVE_NAME)


def load_masters():
    global _masters
    err, res = load(SAVE_NAME)
    if not err:
        _masters = res


load_masters()