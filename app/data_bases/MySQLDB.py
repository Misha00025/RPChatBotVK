import pymysql


class MySQLDB:

    def __init__(self, dbname: str, user: str, password: str, host: str, port: str):
        self._dbname = dbname
        self._user = user
        self._pwd = password
        self._host = host
        self._port = int(port)
        self._connect()

    def _connect(self):
        self.__connection = pymysql.connect(database=self._dbname,
                                            user=self._user,
                                            password=self._pwd,
                                            host=self._host,
                                            port=self._port,
                                            charset='utf8',
                                            cursorclass=pymysql.cursors.SSCursor)
        self.__cursor = self.__connection.cursor()

    def is_connected(self):
        return self.__connection is not None

    def execute(self, query):
        with self.__connection.cursor() as cursor:
            result = cursor.execute(query)
            self.__connection.commit()
        return result

    def fetchone(self, query):
        with self.__connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
        return result

    def fetchall(self, query):
        with self.__connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
        return result
