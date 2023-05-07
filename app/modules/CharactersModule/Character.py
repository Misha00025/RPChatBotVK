

class Character:

    def __init__(self, name=""):
        self.fields = {}
        self.fields["name"] = name
        self.fields["strong"] = 0
        self.fields["vitality"] = 0
        self.fields["agility"] = 0


    def get_fields(self) -> dict:
        return self.fields