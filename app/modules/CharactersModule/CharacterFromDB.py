from .Character import Character
from app import database


class CharacterFromDB:

    def __init__(self):
        self.db = database

    def create_character(self, user_id, character_name):
        pass

    def get_characters(self, user_id) -> [Character]:
        pass




