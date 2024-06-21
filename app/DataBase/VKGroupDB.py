import app


def _save_group(self):
    res = app.database.fetchone(f"SELECT * FROM vk_group WHERE vk_group_id = '{self.group_id}'")
    if res is None:
        app.database.execute(f"INSERT INTO vk_group(vk_group_id, group_name) "
                             f"VALUES ('{self.group_id}', '{self.group_name}')")
    else:
        app.database.execute(f"UPDATE vk_group SET group_name='{self.group_name}' "
                             f"WHERE vk_group_id='{self.group_id}'")