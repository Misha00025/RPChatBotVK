import sqlite3


class DBManager():

    def __init__(self, db_name):
        self._connect = sqlite3.connect(db_name)
        self._cursor = self._connect.cursor()

    def create_table(self, name: str, fields: [str]):
        columns = ""
        for field in fields:
            columns += ", "
            columns += field + " TEXT"
        self._cursor.execute(f"CREATE TABLE if not exists {name}(user_id{columns})")

    def insert(self, table, keys_with_values:{}) -> bool:
        values = ""
        keys = list(keys_with_values.keys())
        keys_str = str(keys)
        keys_str = keys_str[1:len(keys_str)-1]
        for key in keys:
            if values != "":
                values += ", "
            values += f"'{str(keys_with_values[key])}'"

        # print(keys_str)
        # print(values)

        self._cursor.execute(f"INSERT INTO {table}({keys_str})"
                             f"VALUES ({values});")




    def find(self, table, keys_with_values=None) -> dict:
        filter = ""
        if keys_with_values:
            keys = list(keys_with_values.keys())
            for key in keys:
                if filter != "":
                    filter += " AND "
                else:
                    filter += "WHERE "
                filter += f"{key} = '{keys_with_values[key]}'"
        res = self._cursor.execute(f"SELECT * FROM {table} {filter}").fetchone()
        return res


