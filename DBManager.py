import sqlite3


class DBManager():

    def __init__(self, db_name):
        self._connect = sqlite3.connect(db_name)
        self._cursor = self._connect.cursor()

    def create_table(self, name: str, fields: [str]):
        columns = ""
        for field in fields:
            columns += ", "
            columns += field
        self._cursor.execute(f"CREATE TABLE {name}(user_id{columns})")

