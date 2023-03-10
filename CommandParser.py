

class CommandParser():

    def __init__(self, commands: [str], prefix="!"):

        self._prefix = prefix
        self._commands = commands
        print(self._commands)

    def find_commands(self, message: str) -> [(str, str)]:
        '''
        :param message:
        :return list of command with parameters:
        '''

        # print(message)
        commands_and_parameters = []

        while True:
            prefix_position = message.find(self._prefix)

            if prefix_position == -1:
                return commands_and_parameters

            end_of_line_position = message.find("\n", prefix_position)
            if end_of_line_position <= 0:
                end_of_line_position = len(message)

            line = message[prefix_position:end_of_line_position].lower()
            message = message[end_of_line_position+1:]

            command_and_parameters = self.find_command_in_line(line)
            if command_and_parameters == None:
                continue

            commands_and_parameters.append(command_and_parameters)

    def find_command_in_line(self, line: str) -> {str, str}:
        command_start = 0
        command_end = 0

        for command_from_list in self._commands:
            command_start = line.find(command_from_list)
            if command_start != -1:
                command_end = command_start + len(command_from_list)
                break

        if command_start == -1:
            return None

        command = line[command_start:command_end]
        parameters = line[command_end:].strip()
        print(f'Command: {command}, Parameters: {parameters}')
        command_and_parameters = (command, parameters)
        # print(command_and_parameters)
        return command_and_parameters

