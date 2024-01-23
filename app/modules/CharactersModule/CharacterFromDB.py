from .Character import Character
from app import database


table_name = "players_character"


class CharacterFromDB:

    def __init__(self, owner, character_id = None, character: Character = None):
        super().__init__()
        self.owner = owner
        self.db = database
        self.character: Character = character
        if character is None:
            self.character = self._find_character(character_id)


    def _find_character(self, character_id):
        query = f"SELECT name, items FROM {table_name} " \
                f'WHERE "owner_id"="{self.owner.get_user_id()}" AND ' \
                f'id="{character_id}"'
        answer = self.db.fetchone(query)
        if answer is None:
            return Character()
        character = Character(answer[0])
        character.id = character_id
        character.items = answer[1]
        return character

    def save(self):
        user = self.owner
        name = self.character.name
        query = f"INSERT INTO {table_name}(owner_id, id, name) VALUES " \
                f"(\"{user.get_user_id()}\", " \
                f"{CharacterFromDB.get_last_character_id(user) + 1}, " \
                f"\"{name}\");"
        self.db.execute(query)

    @staticmethod
    def get_all_characters(user):
        query = f"SELECT id, name FROM {table_name} WHERE owner_id = \"{user.get_user_id()}\""
        characters = database.fetchall(query)
        if len(characters) == 0:
            return "У вас ещё нет ни одного персонажа. \n" \
                   "Если хотите создать своего первого персонажа," \
                   "то используйте команду: персонаж создать <имя_нового_персонажа>"
        message = "У вас есть следующие персонажи:\n"
        for character in characters:
            print(character)
            message += f"{character[0]}. {character[1]}\n"
        return message

    @staticmethod
    def get_last_character_id(user) -> int:
        query = f"SELECT id FROM {table_name} WHERE owner_id = \"{user.get_user_id()}\";"
        res = database.fetchall(query)
        if res is None or len(res) == 0:
            return 0
        return int(res[len(res)-1][0])