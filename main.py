#!./venv/bin/python

from Arkadia import Arkadia
from config import token, version


application = Arkadia(token=token, version=version)

if __name__ == "__main__":
    application.start()