from .data_bases.PostgreSQLDB import PostgreSQLDB
from .data_bases.MySQLDB import MySQLDB


class DataBase:
    from .. import Logger

    def __init__(self, logger: Logger = None):
        from config import connection_settings
        self._subdb:DataBase = self
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
        return MySQLDB

    def generate_tables(self):
        query = "CREATE TABLE IF NOT EXISTS `vk_user` ("
        query +="`vk_user_id` varchar(20) NOT NULL,"
        query +="`first_name` varchar(30) DEFAULT NULL,"
        query +="`last_name` varchar(30) DEFAULT NULL,"
        query +="`photo_link` varchar(300) DEFAULT NULL,"
        query +="PRIMARY KEY (`vk_user_id`));"
        query += "CREATE TABLE IF NOT EXISTS `vk_group` ("
        query +="`vk_group_id` varchar(20) NOT NULL,`"
        query +="group_name` varchar(50) DEFAULT NULL,"
        query +="`privileges` json DEFAULT NULL,"
        query +="PRIMARY KEY (`vk_group_id`));"
        query += 'CREATE TABLE IF NOT EXISTS `user_group` ('
        query +='`vk_user_id` varchar(20) NOT NULL,'
        query +='`vk_group_id` varchar(20) NOT NULL,'
        query +='`is_admin` tinyint(1) NOT NULL,'
        query +='UNIQUE KEY `vk_user_id` (`vk_user_id`,`vk_group_id`) USING BTREE,'
        query +='KEY `groupe_key` (`vk_group_id`),'
        query +='CONSTRAINT `groupe_key` FOREIGN KEY (`vk_group_id`) REFERENCES `vk_group` (`vk_group_id`) ON DELETE CASCADE ON UPDATE CASCADE,'
        query +='CONSTRAINT `vk_user_key` FOREIGN KEY (`vk_user_id`) REFERENCES `vk_user` (`vk_user_id`));'
        query += "CREATE TABLE IF NOT EXISTS `vk_user_token` ("
        query +="`vk_user_id` varchar(20) NOT NULL,"
        query +="`token` varchar(150) NOT NULL,"
        query +="`last_date` datetime NOT NULL,"
        query +="PRIMARY KEY (`token`),"
        query +="KEY `user_key` (`vk_user_id`),"
        query +="CONSTRAINT `user_key` FOREIGN KEY (`vk_user_id`) REFERENCES `vk_user` (`vk_user_id`) ON DELETE CASCADE ON UPDATE CASCADE);"
        query += "CREATE TABLE IF NOT EXISTS `note` ("
        query +="`group_id` varchar(20) NOT NULL,"
        query +="`owner_id` varchar(20) NOT NULL,"
        query +="`note_id` int NOT NULL AUTO_INCREMENT,"
        query +="`header` varchar(100) NOT NULL,"
        query +="`description` text NOT NULL,"
        query +="`addition_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,"
        query +="`modified_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,"
        query +="PRIMARY KEY (`note_id`,`group_id`,`owner_id`) USING BTREE,"
        query +="UNIQUE KEY `note_id` (`note_id`),"
        query +="KEY `grope_id` (`group_id`),"
        query +="KEY `owner_id` (`owner_id`),"
        query +="CONSTRAINT `note_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `vk_group` (`vk_group_id`) ON DELETE CASCADE ON UPDATE CASCADE,"
        query +="CONSTRAINT `note_ibfk_2` FOREIGN KEY (`owner_id`) REFERENCES `vk_user` (`vk_user_id`) ON DELETE CASCADE ON UPDATE CASCADE);"
        self.execute(query)

