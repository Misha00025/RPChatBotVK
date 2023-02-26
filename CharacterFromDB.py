from DBManager import DBManager
from Character import Character


class CharacterFromDB:

    def __init__(self):
        self.db_name = "character.db"
        self.db_manager = DBManager(self.db_name)
        self.base_character = Character()

        self.db_manager.create_table("Character", ["character_id"] + self.base_character.fields)
        self.db_manager.create_table("User_with_character", ["current_character"])

    def get_characters(self, user_id) -> (int, Character):
        '''
        :param user_id:
        :return characters_count, message:
        '''
        pass


