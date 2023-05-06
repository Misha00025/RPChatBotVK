#!./venv/bin/python
import sys
from contextlib import redirect_stdout

from Arkadia import Arkadia
from config import token, version


if __name__ == "__main__":
    application = Arkadia(token=token, version=version, log_file="log.txt")
    application.start()