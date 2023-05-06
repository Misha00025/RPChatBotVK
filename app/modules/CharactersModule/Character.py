

class Character:

    def __init__(self, name=""):
        self.fields_names = ["имя", "сила", "телосложение", "ловкость", "харизма", "интеллект", "магия"]

        self.fields = {}

        for field_name in self.fields_names:
            self.fields[field_name] = 0
        self.fields[self.fields_names[0]] = name

    def to_dict(self) -> dict:
        return self.fields