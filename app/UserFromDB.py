

class UserFromDB:

    def __init__(self, user_id):
        from app import database
        self.database = database
        if database.is_connected():
            self.user = self._get_from_db(user_id)
            if self.user is None:
                self.user = self._create_user(user_id)
            self._user_id = self.user[0]
            self._is_admin = self.user[1]

    def get_user_id(self):
        return self._user_id

    def is_admin(self):
        return self._is_admin

    def make_admin(self):
        query = f"UPDATE public.vk_user SET is_admin=true WHERE vk_user_id = '{self._user_id}';"
        self.database.execute(query)
        self.user = self._get_from_db(self._user_id)
        self._is_admin = self.user[1]

    def exist(self):
        return self.user is not None

    def _create_user(self, user_id) -> str | None:
        query = f"INSERT INTO public.vk_user(vk_user_id) VALUES ('{user_id}');"
        self.database.execute(query)
        return self._get_from_db(user_id)

    def _get_from_db(self, user_id) -> str | None:
        query = f"SELECT * FROM public.vk_user WHERE vk_user_id = '{user_id}';"
        return self.database.fetchone(query)
