#!./venv/bin/python
from app.Arkadia import Arkadia
from config import token, version

application = Arkadia(token=token, version=version, log_file="log.txt")

if __name__ == "__main__":
    application.start()
