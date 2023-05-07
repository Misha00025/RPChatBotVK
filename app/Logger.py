import os
import shutil
import sys
import datetime

import config


def _get_datetime():
    return datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')


class Logger:

    def __init__(self):
        self._start_time_str = _get_datetime()
        self._console = sys.stdout
        self._log_file_name = config.log_file_name
        self._datetime_in_console = False
        open(self._log_file_name, "w+")

    def write_errors_in_file(self):
        sys.stderr = open(self._log_file_name, "a")

    def only_write(self, msg: str):
        with open(self._log_file_name, "a") as log_file:
            log_file.write(f"[{_get_datetime()}] {msg}\n")

    def write_and_print(self, msg: str):
        self.only_write(msg)
        self.only_print(msg)

    def only_print(self, msg: str):
        dt = ""
        if self._datetime_in_console:
            dt = f"[{_get_datetime()}] "
        self._console.write(f"{dt}{msg}\n")

    def write_datetime_in_console(self):
        self._datetime_in_console = True

    def save_logs(self):
        if not os.path.exists("logs"):
            os.mkdir("logs")
        shutil.copyfile(self._log_file_name, os.path.join("logs",f"{self._start_time_str}_{self._log_file_name}"))
