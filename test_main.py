#!./venv/bin/python

from Arkadia import Arkadia
from config import version, token


application = Arkadia(token=token, test_mode=True, version=version)

if __name__ == "__main__":
    application.start()