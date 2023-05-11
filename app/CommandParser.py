def _find_in_line(line: str, command, offset: int = 0):
    low_line = line.lower()
    command_pos = low_line.find(command) + offset
    if offset == 0:
        if command_pos <= 0:
            return ""
        line = line[:command_pos]
    else:
        if command_pos == offset - 1:
            return ""
        line = line[command_pos:]
    return line.strip()


class CommandParser():

    def __init__(self, commands: [str], prefix="!"):

        self._start = prefix
        self._commands = commands
        # print(self._commands)

    def find_command_lines(self, message: str) -> [str]:
        lines = message.split("\n")
        lines_with_commands: [str] = []
        for line in lines:
            start_pos = line.find(self._start)
            if start_pos == -1:
                continue
            if self._start == "":
                start_pos = -1
            lines_with_commands.append(line[start_pos+1:])
        return lines_with_commands

    def find_prefix_in_line(self, line: str, command: str = "") -> str:
        if command == "":
            command = self.find_command_in_line(line)
        return _find_in_line(line, command, 0)

    def find_parameters_in_line(self, line: str, command: str = "") -> str:
        if command == "":
            command = self.find_command_in_line(line)
        return _find_in_line(line, command, len(command))

    def find_command_in_line(self, line: str):
        line = line.lower()
        for command_from_list in self._commands:
            command_start = line.find(command_from_list)
            if command_start == -1:
                continue
            return command_from_list
        return None
