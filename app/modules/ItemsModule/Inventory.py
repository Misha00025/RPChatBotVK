from app.tdn.api.items import get_items_api


class Inventory:
    def __init__(self, owner_id) -> None:
        self.api = get_items_api()
        self.owner_id = owner_id

    def get_item(self, name):
        return self.api.get_item(name, self.owner_id)
    
    def get_items(self):
        return self.api.get_items(self.owner_id)
        
