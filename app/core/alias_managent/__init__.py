from .AliasMaker import AliasMaker


_instance: AliasMaker = None


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
