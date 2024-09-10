from requests import Response
from app.tdn import TdnSession
from app.tdn.api import TdnApi
        

COMMAND = "items/"
OWNER_ID = "owner_id"
NAME = "name"
DESCRIPTION = "description"
AMOUNT = "amount"
ITEM_FIELDS = ["id", NAME, DESCRIPTION]


class ParsedItem:
    id: int = 0
    name: str = ""
    description: str = ""
    amount: int | None = None

    def __str__(self) -> str:
        return str({"id": self.id, NAME: self.name, DESCRIPTION: self.description, AMOUNT: self.amount})

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def get_from_json(json: dict):
        for field in ITEM_FIELDS:
            if field not in json.keys():
                return None
        item = ParsedItem()
        item.id = json["id"]
        item.name = json[NAME]
        item.description = json[DESCRIPTION]
        if AMOUNT in json.keys():
            item.amount = int(json[AMOUNT])
        return item


class TdnItemsApi(TdnApi):
    def __init__(self, tdn: TdnSession):
        super().__init__(tdn)

    def get_item(self, name, owner_id = None):
        params = {}
        if owner_id is not None:
            params[OWNER_ID] = owner_id
        response = self.session.get(COMMAND+str(name), params)
        item = ParsedItem.get_from_json(response.json())
        return item is not None, item

    def get_items(self, owner_id = None):
        params = {}
        if owner_id is not None:
            params[OWNER_ID] = owner_id
        response = self.session.get(COMMAND, params)
        if not response.ok:
            return False, response.text
        items = response.json()["items"]
        result = [ParsedItem.get_from_json(item) for item in items]
        return True, result
    
    def add_item(self, name, user_id, amount=1):
        response = self.session.post(COMMAND+name, {AMOUNT: amount}, {OWNER_ID: user_id})
        return response.ok, response.text

    def update_item(self, name, owner_id, amount):
        response = self.session.put(COMMAND+name, {AMOUNT: amount}, {OWNER_ID: owner_id})
        return response.ok, ParsedItem.get_from_json(response.json())

    def remove_item(self, name, user_id):
        response = self.session.delete(COMMAND+name, {OWNER_ID: user_id})
        return response.ok, response.text
    
    def create_item(self, name, description = "None") -> tuple[bool, ParsedItem]:
        response = self.session.post(COMMAND+"create", {NAME: name, DESCRIPTION: description})
        json = response.json()
        res = response.text
        if "created_item" in json.keys():
            res = ParsedItem.get_from_json(json["created_item"])
        return response.ok, res


_api: TdnItemsApi | None = None


def get_items_api() -> TdnItemsApi:
    global _api
    if _api is None:
        from app.tdn import get_session
        _api = TdnItemsApi(get_session())
    return _api




