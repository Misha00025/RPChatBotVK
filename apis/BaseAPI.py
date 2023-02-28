

class BaseAPI:

    def __init__(self):
        self.events = {}

        self.commands = ["привет", "помощь", "пока"]

    def assembly_message(self, user_id, commands_with_parameters: [(str, str)]) -> str:
        def say_hello(self):
            return f'Здравствуйте, меня зовут {self.name}. Если хотите узнать меня лучше, отправьте команду "Расскажи о себе" и я поведаю Вам больше'

        def say_about_yourself(self):
            return f'Моё имя -- {self.name}. Я -- бот-ассистент для текстовых ролевых игр в чатах. ' \
                   'Я ещё нахожусь в разработке, поэтому знаю только эти команды: \n\n' \
                   '1. Расскажи о себе \n\n ' \
                   'Ещё меня научили здороваться и прощаться, и я рада этому! ' \
                   'Хочу всегда учиться чему-то новому, чтобы становиться всё полезнее и полезнее!'
        for command, parameters in commands_with_parameters:
            if command == "привет":
                return say_hello()
            elif command == "расскажи о себе":
                return say_about_yourself()
            elif command == "пока":
                return "До свидания"

    def has_commands(self, commands_with_parameters) -> bool:
        for command, parameters in commands_with_parameters:
            if command in self.commands:
                return True
        return False


    def void_command(self, user_id, parameters) -> str:
        return "Команда ничего не делает, увы :С"