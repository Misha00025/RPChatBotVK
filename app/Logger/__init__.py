import os
import shutil
import sys
import datetime

import config


def _get_datetime():
    return datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')


def _get_datetime_to_filename():
    return datetime.datetime.now().strftime('%d.%m.%Y %H_%M_%S')


_start_time_str = _get_datetime()
_console = sys.stdout
_log_path = "logs"
_log_backups = os.path.join(_log_path, "backups")
_log_file_name = config.log_file_name
_log_file = os.path.join(_log_path, _log_file_name)
_datetime_in_console = False
open(_log_file, "w+")


def write_errors_in_file():
    sys.stderr = open(_log_file, "a")


def only_write(msg):
    with open(_log_file, "a") as log_file:
        try:
            msg = str(msg)
            msg = msg.replace('\U0001f4a5', 'BOOM!')
            msg = msg.replace("\U0001f480", 'OPS!')
            log_file.write(f"[{_get_datetime()}] {msg}\n")
        except Exception as err:
            log_file.write(f"[{_get_datetime()}] {err}\n")


def write_and_print(msg):
    only_print(msg)
    only_write(msg)


def only_print(msg):
    dt = ""
    if _datetime_in_console:
        dt = f"[{_get_datetime()}] "
    _console.write(f"{dt}{msg}\n")


def write_datetime_in_console():
    _datetime_in_console = True


def save_logs():
    if not os.path.exists(_log_backups):
        os.mkdir(_log_backups)
    file_path = os.path.join(_log_backups, f"{_get_datetime_to_filename()}_{_log_file_name}")
    shutil.copyfile(_log_file, file_path)
