from vk_api.longpoll import Event

from .DiceController import DiceController
from app.modules.BaseModule.BaseAPI import BaseAPI


class DicesAPI(BaseAPI):

    def __init__(self):
        self.commands = ["dice ", "d", "куб ", "к"]
        super().__init__(self.commands)
        self.dice_controller = DiceController()

    def assembly_message(self, event: Event, command_lines: [str]) -> str:
        message = ""
        for line in command_lines:
            command = self.cp.find_command_in_line(line)
            parameters = self.cp.find_parameters_in_line(line, command)
            prefix = self.cp.find_prefix_in_line(line, command)
            if command in self.commands:
                message += self.dice_controller.execute_command(command, parameters, prefix) + '\n'
        return message