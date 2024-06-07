#!./venv/bin/python
from app.modules.BaseModule.BaseAPI import BaseAPI
from app.modules.NotesModule.NotesAPI import NotesAPI


def dialog():
    from app.Tasia import Tasia
    from config import version
    application = Tasia(version=version)
    application.start()


def auto(api: BaseAPI, commands: list):
    from app.UserFromDB import UserFromDB
    user = UserFromDB('173745999')
    class Ev:
        group_id = "-101"
    user.from_event = Ev()
    for command in commands:
        print(f"Command: {command}")
        print(f"Answer: {api.assembly_message(user, command, "\n".join(command))}")


def db_test():
    from app import database
    user_id = 'test_user_2'
    query = f"INSERT INTO vk_user(vk_user_id) VALUES ('{user_id}');"
    print(f"Status: {database.execute(query)}")
    # query = f"INSERT INTO vk_user(vk_user_id) VALUES ('{user_id}');"
    # print(f"Status: {database.execute(query)}")
    query = f"DELETE FROM vk_user WHERE vk_user_id = '{user_id}';"
    print(f"Status: {database.execute(query)}")




if __name__ == "__main__":
    import app
    app.start(cmd_prefix="!")
    # db_test()
    # api = NotesAPI()
    # print(api.commands)
    # auto(api, [["заметки записать: заметка1", "Я проверяю заметку"], ["заметки"], ["заметки удалить 1"]])
    # dialog()
