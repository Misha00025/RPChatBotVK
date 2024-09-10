from app.tdn.api.items import get_items_api


class Inventory:
    def __init__(self, owner_id) -> None:
        self.api = get_items_api()
        self.owner_id = owner_id

    def get_item(self, name):
        return self.api.get_item(name, self.owner_id)
    
    def get_items(self):
        return self.api.get_items(self.owner_id)
    
    def add_item(self, name, amount):
        return self.update_item(name, amount)

    def remove_item(self, name, amount):
        have, item = self.get_item(name)
        if not have:
            return False, ""
        if item.amount <= amount:
            self.api.remove_item(name, self.owner_id)
            return True, None
        return self.update_item(name, -amount)

    def update_item(self, name, amount):
        have, item = self.get_item(name)
        if not have:
            ok, _ = self.api.get_item(name)
            if not ok:
                ok, _ = self.api.create_item(name, name)
        if not have:
            return self.api.add_item(name, self.owner_id, amount)
        else:
            amount = item.amount + amount
            return self.api.update_item(name, self.owner_id, amount)
