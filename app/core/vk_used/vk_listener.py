from .vk_connector import get_connector
from vk_api.longpoll import VkLongPoll


# TODO: изменить способ обработки событий. Сделать так, чтобы события проверялись на выполнение определённых условий, а не только на определнный event.
class VkListener:
    def __init__(self):
        self.actions = {}
        self._connector = get_connector()

    def start_listen(self):
        longpoll = VkLongPoll(self._connector.get_session())
        for event in longpoll.listen():
            if event.type in self.actions.keys():
                if hasattr(event, "message"):
                    event.text = event.message
                for action in self.actions[event.type]:
                    action(event)

    def add_action_to_event(self, action, event_type):
        if event_type not in self.actions.keys():
            self.actions[event_type] = []
        self.actions[event_type].append(action)

    def clear(self):
        self.actions.clear()

