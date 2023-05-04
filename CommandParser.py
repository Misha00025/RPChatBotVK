

class CommandParser():

    def __init__(self, commands: [str], prefix="!"):

        self._start = prefix
        self._commands = commands
        print(self._commands)

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
        command_start = line.find(command)
        if command_start <= 0:
            return ""
        return line[:command_start-1]

    def find_command_in_line(self, line: str) -> str | None:
        for command_from_list in self._commands:
            command_start = line.find(command_from_list)
            if command_start == -1:
                continue
            return command_from_list
        return None

    def find_parameters_in_line(self, line: str, command: str = "") -> str:
        if command == "":
            command = self.find_command_in_line(line)
        command_end = line.find(command) + len(command)
        if command_end == len(command)-1:
            return ""
        return line[command_end:]