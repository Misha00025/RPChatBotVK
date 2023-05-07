import psycopg2
from psycopg2 import Error




class DataBase:
    from app.Logger import Logger

    def __init__(self, logger: Logger):
        from config import connection_settings

        dbname = connection_settings["DataBaseName"]
        user = connection_settings["User"]
        password = connection_settings["Password"]
        host = connection_settings["Host"]
        port = connection_settings["Port"]

        self.logger = logger
        self._connect(dbname, user, password, host, port)

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
            return 1, error

    def _disconnect(self):
        """
        Закрывает соединение с базой данной.
        """
        self.__cursor.close()
        self.__connection.close()
        self.logger.write_and_print(f'DataBase.connect(): соединение с базой данных закрыто;')