#!./venv/bin/python
from app.modules.BaseModule.BaseAPI import BaseAPI


def auto(api: BaseAPI, commands: list):
    from app.core.User import User
    user = User('173745999', "-101")
    class Ev:
        group_id = "-101"
    user.from_event = Ev()
    for command in commands:
        print(f"Command: {command}")
        print(f"Answer: {api.assembly_message(user, command, "\n".join(command))}")


if __name__ == "__main__":
    import app
    app.start(cmd_prefix="!")
    # db_test()
    # api = NotesAPI()
    # print(api.commands)
    # auto(api, [["заметки записать: заметка1", "Я проверяю заметку"], ["заметки"], ["заметки удалить 1"]])
    # dialog()
