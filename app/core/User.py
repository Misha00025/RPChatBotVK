

class User:

    def __init__(self, user_id, group_id, is_admin=False):
        self.group_id = group_id
        self._user_id = user_id
        self._is_admin = is_admin

    def get_user_id(self):
        return self._user_id

    def is_admin(self):
        return self._is_admin

    def exist(self):
        return self.user is not None
