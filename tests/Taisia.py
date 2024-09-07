from app.Arkadia import Arkadia


class Taisia(Arkadia):
    def __init__(self):
        super().__init__("1.1.1", "!")

    def start(self):
        self._events_listen()

    def _get_listener_and_sender(self):
        from .TestListener import TestListener
        from .TestSender import TestSender
        return TestListener(), TestSender()

