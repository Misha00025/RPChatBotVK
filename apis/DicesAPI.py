from DiceController import DiceController
from apis.BaseAPI import BaseAPI


class DicesAPI(BaseAPI):

    def __init__(self):
        self.dice_controller = DiceController()

        self.commands = ["dice ", "d", "куб ", "к"]

    def assembly_message(self, user_id, commands_with_parameters: [(str, str)]) -> str:
        message = ""
        for command, parameters in commands_with_parameters:
            if command in self.commands:
                message += self.dice_controller.execute_command(command, parameters) + '\n'
        return message