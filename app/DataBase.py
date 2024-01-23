from .data_bases.PostgreSQLDB import PostgreSQLDB
from .data_bases.MySQLDB import MySQLDB


class DataBase:
    from app.Logger import Logger

    def __init__(self, logger: Logger = None):
        from config import connection_settings
        if connection_settings is not None:
            self.type = connection_settings["Type"]
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
        return self._subdb.is_connected()

    def execute(self, query):
        try:
            return self._subdb.execute(query)
        except Exception as err:
            self.logger.write_and_print(err)
            return None

    def fetchone(self, query):
        try:
            return self._subdb.fetchone(query)
        except Exception as err:
            self.logger.write_and_print(err)
            return None

    def fetchall(self, query):
        try:
            return self._subdb.fetchall(query)
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
            self._subdb = self._get_connector()(dbname=dbname,
                                     user=user,
                                     password=password,
                                     host=host,
                                     port=port)
            self.logger.write_and_print(f'DataBase.connect():\033[32m соединение установлено;\033[0m\n')
            return 0, dbname
        except Exception as error:
            self.logger.write_and_print(f'\033[31mDataBase.connect(): не удается установить соединение с базой данных: {error}\033[0m')
            self._subdb = None
            return 1, error

    def _disconnect(self):
        """
        Закрывает соединение с базой данной.
        """
        self._subdb = None
        self.logger.write_and_print(f'DataBase.connect(): соединение с базой данных закрыто;')

    def _get_connector(self):
        connector = None
        type = self.type
        connectors = {
            "PostgreSQL": PostgreSQLDB,
            "MySQL": MySQLDB
        }
        if type in connectors.keys():
            connector = connectors[type]
        return connector
