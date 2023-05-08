

class Character:

    def __init__(self, name=""):
        self.owner = None
        self.id = None
        self.name = name
        self.properties: {} = None
        self.stats: {} = None
        self.items: {} = None

    def to_message(self):
        if not self.exist():
            return "Такого персонажа не существует!"
        message = f"Персонаж {self.id}:\n" \
                  f"--Имя: {self.name}\n" \
                  f"--Предметы: {self.items}"
        return message

    def exist(self):
        return self.id is not None