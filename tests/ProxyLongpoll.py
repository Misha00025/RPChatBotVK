from vk_api.longpoll import Event, VkEventType, VkMessageFlag
from .TEvent import TEvent


class ProxyLongpoll:
    def __init__(self):
        pass

    def listen(self) -> list[Event]:
        events = []
        last_id = 0
        last_id, events = self.gen_events("test_user", last_id, events)
        last_id, events = self.gen_events("tester", last_id, events)
        return events


    def gen_events(self, _from, last_id, events: list = []):
        template = [VkEventType.MESSAGE_NEW, 0, VkMessageFlag.UNREAD, _from, "", "", "", "", ""]
        messages = [
            # "/start",
            # "/d20", "/d20 + 1", "/d20 + 2",
            # "/заметки записать: Тест <br> Тест",
            "/инвентарь добавить меч", "/инвентарь", "/инвентарь удалить меч 2", "/инвентарь",
            "/инвентарь добавить деньги 100", "/инвентарь", "/инвентарь удалить деньги 50",
            "/кошель", "/кошель дать 200", "/кошель", "/кошель забрать 300", "/кошель"
        ]
        for msg in messages:
            last_id += 1
            raw = template.copy()
            raw[1], raw[5] = last_id, msg
            events.append(TEvent(raw))
        return last_id, events