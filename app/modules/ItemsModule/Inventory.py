from app.tdn.api import character
from app.core.character_owners import as_character


class Inventory:
    def __init__(self, owner_id) -> None:
        self.api = character(as_character(owner_id)).items()
        self.owner_id = owner_id

    def get_item(self, name) -> dict:
        items = self.get_items()
        for item in items:
            if item["name"] == name:
                return item
        return None
    
    def get_items(self):
        res = self.api.get()
        if res.ok:
            return res.json()["items"]
        return []

    def change_item_amount(self, name, amount):
        item = self.get_item(name)
        if item is None:
            new_amount = amount
            if new_amount <= 0:
                return False
        else:
            new_amount = item["amount"] + amount
        return self.update_item(name, new_amount)

    def update_item(self, name, amount, description = None):
        item = self.get_item(name)
        if item is None:
            item = {
                "name": name,
                "amount": int(amount),
                "description": description if description is not None else ""
            }
            res = self.api.post(**item)
            return res.ok
        else:
            if description != None:
                item["description"] = description
            data = {
                "name": item["name"],
                "amount": int(amount),
                "description": item["description"],
            }
            res = self.api.put(item["id"], data)
            return res.ok
        
