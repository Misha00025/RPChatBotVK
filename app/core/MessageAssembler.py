from app.core.CommandParser import CommandParser
from app.core.Loaders import load_modules, load_commands
from app.core.User import User
from vk_api.longpoll import Event


class MessageAssembler:
    def __init__(self, cmd_prefix):
        self._modules = load_modules(self.has_correct_api)
        self._commands = load_commands(self._modules, self.has_correct_api)
        self.command_parser = CommandParser(self._commands, cmd_prefix)

    def assembly_message(self, event: Event, group_id, user_is_admin=False):
        request = event.text
        command_lines: list = self.command_parser.find_command_lines(request)
        user = User(event.user_id, group_id, user_is_admin)
        message = self._assembly_message(user, command_lines, request)
        return message

    def _assembly_message(self, user: User, command_lines: list, request):
        message = ""
        for module in self._modules:
            if self.has_correct_api(module) and module.has_commands(command_lines):
                module_message = module.assembly_message(user, command_lines, request)
                if module_message is None:
                    continue
                message += module_message + "\n\n"
        return message

    @staticmethod
    def has_correct_api(module) -> bool:
        return hasattr(module, "commands") and \
            hasattr(module, "assembly_message") and \
            hasattr(module, "has_commands")


_assembler = None


def get_assembler():
    global _assembler
    from app import global_cmd_prefix
    if _assembler is None:
        _assembler = MessageAssembler(global_cmd_prefix)
    return _assembler
