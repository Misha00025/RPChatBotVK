from DBManager import DBManager
from Character import Character


class CharacterFromDB:

    def __init__(self):
        self.db_name = "db/characters.db"
        self.db_manager = DBManager(self.db_name)
        self.base_character = Character()
        self.table_name = "Character"

        self.db_manager.create_table(self.table_name, ["character_id"] + self.base_character.fields_names)
        self.db_manager.create_table("User_with_character", ["current_character"])

    def create_character(self, user_id, character_name):
        new_character = Character(character_name)

        parameters = new_character.to_dict()
        parameters["user_id"] = user_id
        parameters["character_id"] = 1

        self.db_manager.insert(self.table_name, parameters)


    def get_characters(self, user_id) -> [Character]:
        '''
        :param user_id:
        :return characters_count, message:
        '''

        res = self.db_manager.find(self.table_name, {"user_id": user_id})

        return res




