#!./venv/bin/python

from Tasia import Tasia
from config import version, token


application = Tasia(version=version)

if __name__ == "__main__":
    application.start()