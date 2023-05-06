#!./venv/bin/python

from app.Tasia import Tasia
from config import version

application = Tasia(version=version)

if __name__ == "__main__":
    application.start()