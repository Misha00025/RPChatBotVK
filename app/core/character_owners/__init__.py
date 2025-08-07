
characters = {}


def set_character(user_id, character_id):
    characters[str(user_id)] = int(character_id)

def as_character(user_id) -> int:
    if user_id not in characters:
        return -1
    return characters[str(user_id)]

