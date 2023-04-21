from Arkadia import Arkadia
from config import token


version = "0.2.0"

application = Arkadia(token=token, version=version)

if __name__ == "__main__":
    application.start()