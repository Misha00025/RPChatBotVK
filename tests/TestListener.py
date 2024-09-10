from app.core.vk_used.vk_listener import VkListener
from .ProxyLongpoll import ProxyLongpoll


class TestListener(VkListener):
    def __init__(self):
        self.actions = {}

    def start_listen(self):
        longpoll = ProxyLongpoll()
        for event in longpoll.listen():
            if event.type in self.actions.keys():
                if hasattr(event, "message"):
                    event.text = event.message
                for action in self.actions[event.type]:
                    action(event)