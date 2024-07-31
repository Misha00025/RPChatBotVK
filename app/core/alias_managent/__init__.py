from .AliasMaker import AliasMaker
from app.core.DataSaver import save, load


_instance: AliasMaker = None
SAVE_NAME = "alias"


def _get_instance():
    global _instance
    if _instance is None:
        _instance = AliasMaker()
    return _instance


def get_alias(user_id):
    inst = _get_instance()
    return inst.get_alias(user_id)


def set_alias(user_id, alias):
    inst = _get_instance()
    inst.set_alias(user_id, alias)
    save_alias()


def save_alias():
    save(_get_instance(), SAVE_NAME)


def load_alias():
    global _instance
    err, res = load(SAVE_NAME)
    if not err:
        _instance = res


load_alias()