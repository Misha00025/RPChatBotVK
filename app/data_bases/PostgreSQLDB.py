import psycopg2


class PostgreSQLDB:

    def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
        self.__connection = psycopg2.connect(dbname=dbname,
                                             user=user,
                                             password=password,
                                             host=host,
                                             port=port)
        self.__cursor = self.__connection.cursor()

    def execute(self, query):
        with self.__connection:
            self.__cursor.execute(query)

    def fetchone(self, query):
        with self.__connection:
            self.__cursor.execute(query)
            result = self.__cursor.fetchone()
        return result

    def fetchall(self, query):
        with self.__connection:
            self.__cursor.execute(query)
            result = self.__cursor.fetchall()
        return result

