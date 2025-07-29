

class AliasMaker:
    def __init__(self, alias_list = None):
        if alias_list is None:
            alias_list = {}
        self._alias_list = alias_list

    def set_alias(self, user_id, alias):
        self._alias_list[user_id] = alias

    def get_alias(self, user_id):
        if user_id not in self._alias_list.keys():
            return user_id
        return self._alias_list[user_id]
