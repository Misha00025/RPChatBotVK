from vk_api.vk_api import VkApi, VkApiMethod
from . import vk_settings
from .vk_group_info import VkGroupInfo


class VkConnector:
    def __init__(self, token):
        self.token = token

    def _init_vk_session(self):
        self._vk_session = VkApi(token=self.token)
        self._vk: VkApiMethod = self._vk_session.get_api()
        self._info = self.get_api().groups.getById(fields=["contacts"])

    def get_info(self) -> VkGroupInfo:
        info = VkGroupInfo(self._info)
        return info

    def get_session(self) -> VkApi:
        return self._vk_session

    def get_api(self) -> VkApiMethod:
        return self._vk

    def connect(self):
        from app.Logger import write_and_print
        try:
            write_and_print("Выполняется подключение к серверам VK")
            self._init_vk_session()
        except Exception as err:
            write_and_print(f"При подключении произошла ошибка: {err}")
            return 1
        finally:
            write_and_print("Подключение прошло успешно!")
            return 0


_instance: VkConnector = None


def get_connector() -> VkConnector:
    global _instance
    cs = vk_settings
    if _instance is None:
        _instance = VkConnector(cs.token)
        _instance.connect()
    return _instance