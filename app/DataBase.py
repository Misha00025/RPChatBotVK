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
            self._subdb = self
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
        query = "CREATE TABLE IF NOT EXISTS `vk_user` (" \
                "`vk_user_id` varchar(20) NOT NULL," \
                "`first_name` varchar(30) DEFAULT NULL," \
                "`last_name` varchar(30) DEFAULT NULL," \ 
                "`photo_link` varchar(300) DEFAULT NULL," \
                "PRIMARY KEY (`vk_user_id`));"
        query += "CREATE TABLE IF NOT EXISTS `vk_group` (" \
                "`vk_group_id` varchar(20) NOT NULL,`" \
                "group_name` varchar(50) DEFAULT NULL," \
                "`privileges` json DEFAULT NULL," \
                "PRIMARY KEY (`vk_group_id`));"
        query += 'CREATE TABLE IF NOT EXISTS `user_group` (' \
                '`vk_user_id` varchar(20) NOT NULL,' \ 
                '`vk_group_id` varchar(20) NOT NULL,' \
                '`is_admin` tinyint(1) NOT NULL,' \
                'UNIQUE KEY `vk_user_id` (`vk_user_id`,`vk_group_id`) USING BTREE,' \ 
                'KEY `groupe_key` (`vk_group_id`),' \
                'CONSTRAINT `groupe_key` FOREIGN KEY (`vk_group_id`) REFERENCES `vk_group` (`vk_group_id`) ON DELETE CASCADE ON UPDATE CASCADE,' \
                'CONSTRAINT `vk_user_key` FOREIGN KEY (`vk_user_id`) REFERENCES `vk_user` (`vk_user_id`));'
        query += "CREATE TABLE IF NOT EXISTS `vk_user_token` ("\
                "`vk_user_id` varchar(20) NOT NULL,"\
                "`token` varchar(150) NOT NULL,"\
                "`last_date` datetime NOT NULL,"\
                "PRIMARY KEY (`token`),"\
                "KEY `user_key` (`vk_user_id`),"\
                "CONSTRAINT `user_key` FOREIGN KEY (`vk_user_id`) REFERENCES `vk_user` (`vk_user_id`) ON DELETE CASCADE ON UPDATE CASCADE);"
        query += "CREATE TABLE IF NOT EXISTS `note` ("\
                "`group_id` varchar(20) NOT NULL,"\
                "`owner_id` varchar(20) NOT NULL,"\
                "`note_id` int NOT NULL AUTO_INCREMENT,"\
                "`header` varchar(100) NOT NULL,"\
                "`description` text NOT NULL,"\
                "`addition_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,"\
                "`modified_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,"\
                "PRIMARY KEY (`note_id`,`group_id`,`owner_id`) USING BTREE,"\
                "UNIQUE KEY `note_id` (`note_id`),"\
                "KEY `grope_id` (`group_id`),"\
                "KEY `owner_id` (`owner_id`),"\
                "CONSTRAINT `note_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `vk_group` (`vk_group_id`) ON DELETE CASCADE ON UPDATE CASCADE,"\
                "CONSTRAINT `note_ibfk_2` FOREIGN KEY (`owner_id`) REFERENCES `vk_user` (`vk_user_id`) ON DELETE CASCADE ON UPDATE CASCADE);"
        self.execute(query)

