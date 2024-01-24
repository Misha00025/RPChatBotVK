#!./venv/bin/python
from app.modules.BaseModule.BaseAPI import BaseAPI
from app.modules.CharactersModule.CharacterAPI import CharacterAPI
from app.modules.NotesModule.NotesAPI import NotesAPI


def dialog():
    from app.Tasia import Tasia
    from config import version
    application = Tasia(version=version)
    application.start()


def auto(api: BaseAPI, commands: []):
    from app.UserFromDB import UserFromDB
    user = UserFromDB('test_user')
    for command in commands:
        print(f"Command: {command}")
        print(f"Answer: {api.assembly_message(user, [command])}")


def db_test():
    from app import database
    user_id = 'test_user'
    query = f"INSERT INTO vk_user(vk_user_id) VALUES ('{user_id}');"
    print(f"Status: {database.execute(query)}")




if __name__ == "__main__":
    # db_test()
    auto(NotesAPI(), ["заметки записать: заметка1", "заметки", "заметки удалить 1"])
    # dialog()
