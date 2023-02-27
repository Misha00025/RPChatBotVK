

class Character:

    def __init__(self):
        self.fields_names = ["strong", "body", "agility", "charm", "intellect", "arcane"]

        self.fields = {}

        for field_name in self.fields_names:
            self.fields[field_name] = 0


character = Character()

print(character.fields)