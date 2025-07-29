from app.core.User import User
from app.model.character import Character


user_character: dict[int, int] = {}


def my_character(user: User) -> Character:
    user_id = int(user.get_user_id())
    if user_id not in user_character.keys():
        return None
    character_id = user_character[user_id]
    return Character(character_id)

def set_character(user: User, character_id):
    user_character[int(user.get_user_id())] = character_id

