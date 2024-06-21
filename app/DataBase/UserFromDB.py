from app import database


class UserFromDB:

    def __init__(self, user_id, group_id = None):
        self.group_id = group_id
        self.database = database
        if database.is_connected():
            self.user = self._get_from_db(user_id)
            if self.user is None:
                self.user = self._create_user(user_id)
            try:
                self._user_id = self.user[0]
                self._is_admin = self.user[1]
            except:
                self._user_id = "unnamed"
                self._is_admin = False

    def get_user_id(self):
        if not self.database.is_connected():
            return 0
        return self._user_id

    def is_admin(self):
        if not self.database.is_connected():
            return False
        return self._is_admin

    def make_admin(self):
        query = f"UPDATE vk_user SET is_admin=true WHERE vk_user_id = '{self._user_id}';"
        self.database.execute(query)
        self.user = self._get_from_db(self._user_id)
        self._is_admin = self.user[1]

    def exist(self):
        return self.user is not None

    def _create_user(self, user_id):
        query = f"INSERT INTO vk_user(vk_user_id) VALUES ('{user_id}');"
        self.database.execute(query)
        return self._get_from_db(user_id)

    def _get_from_db(self, user_id):
        query = f"SELECT * FROM vk_user WHERE vk_user_id = '{user_id}';"
        return self.database.fetchone(query)
