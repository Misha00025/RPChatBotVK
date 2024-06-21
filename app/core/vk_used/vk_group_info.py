

class VkGroupInfo:
    def __init__(self, response):
        response: dict = response[0]
        self.id = response["id"]
        self.name = response["name"]
        self.admin_ids = []
        for admin in response["contacts"]:
            self.admin_ids.append(admin["user_id"])

