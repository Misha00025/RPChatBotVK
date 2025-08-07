
from app.core.DataSaver import load, save


_characters = {}
_save_name = "characters"


def set_character(user_id, character_id):
    _characters[str(user_id)] = int(character_id)
    save_characters()

def as_character(user_id) -> int:
    if user_id not in _characters:
        return -1
    return _characters[str(user_id)]


def save_characters():
    save(_characters, _save_name)


def load_characters():
    global _characters
    err, res = load(_save_name)
    if not err:
        _characters = res


load_characters()