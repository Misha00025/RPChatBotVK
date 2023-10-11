import psycopg2
from psycopg2 import Error


class DataBase:
    from app.Logger import Logger

    def __init__(self, logger: Logger = None):
        from config import connection_settings
        if connection_settings is not None:
            dbname = connection_settings["DataBaseName"]
            user = connection_settings["User"]
            password = connection_settings["Password"]
            host = connection_settings["Host"]
            port = connection_settings["Port"]

            self.logger = logger
            if self.logger is None:
                from app.Logger import Logger
                self.logger = Logger()
            self._connect(dbname, user, password, host, port)

    def is_connected(self):
        return self.__connection is not None

    def execute(self, query):
        try:
            with self.__connection:
                self.__cursor.execute(query)
        except Exception as err:
            self.logger.write_and_print(err)
            return None

    def fetchone(self, query):
        try:
            with self.__connection:
                self.__cursor.execute(query)
                result = self.__cursor.fetchone()
            return result
        except Exception as err:
            self.logger.write_and_print(err)
            return None

    def fetchall(self, query):
        try:
            with self.__connection:
                self.__cursor.execute(query)
                result = self.__cursor.fetchall()
            return result
        except Exception as err:
            self.logger.write_and_print(err)
            return None

    def _connect(self, dbname: str, user: str, password: str, host: str, port: str):
        """
        Выполняет подключение к базе данных.
        :return: 0 в случае успешного подключения; 1 при наличии ошибок
        """
        self.logger.write_and_print(f'DataBase.connect(): устанавливаю соединение;')
        try:
            self.__connection = psycopg2.connect(dbname=dbname,
                                                 user=user,
                                                 password=password,
                                                 host=host,
                                                 port=port)
            self.__cursor = self.__connection.cursor()
            self.logger.write_and_print(f'DataBase.connect():\033[32m соединение установлено;\033[0m\n')
            return 0, dbname
        except (Exception, Error) as error:
            self.logger.write_and_print(f'\033[31mDataBase.connect(): не удается установить соединение с базой данных: {error}\033[0m')
            self.__connection = None
            return 1, error

    def _disconnect(self):
        """
        Закрывает соединение с базой данной.
        """
        self.__cursor.close()
        self.__connection.close()
        self.__connection = None
        self.logger.write_and_print(f'DataBase.connect(): соединение с базой данных закрыто;')


