from .Character import Character
from app import database


class CharacterFromDB(Character):

    def __init__(self, owner, character_id = None):
        super().__init__()
        self.db = database
        self.owner = owner
        self._find_character(character_id)

    def _find_character(self, character_id):
        query = f"SELECT character_name, items FROM public.\"character\" " \
                f"WHERE owner_id='{self.owner.get_user_id()}' AND " \
                f"character_id='{character_id}'"
        character = self.db.fetchone(query)
        if character is None:
            return
        self.id = character_id
        self.name = character[0]
        self.items = character[1]

    @staticmethod
    def get_all_characters(user):
        query = f"SELECT character_id, character_name " \
                f"FROM public.\"character\" " \
                f"WHERE owner_id = '{user.get_user_id()}'"
        characters = database.fetchall(query)
        if len(characters) == 0:
            return "У вас ещё нет ни одного персонажа. \n" \
                   "Если хотите создать своего первого персонажа," \
                   "то используйте команду: персонаж создать <имя_нового_персонажа>"
        message = "У вас есть следующие персонажи:\n"
        for character in characters:
            message += f"{character[0]}. {character[1]}\n"
        return message

    @staticmethod
    def get_last_character_id(user) -> int:
        query = f"SELECT character_id FROM public.\"character\" WHERE owner_id = '{user.get_user_id()}';"
        res = database.fetchall(query)
        if len(res) == 0:
            return 0
        return int(res[len(res)-1][0])