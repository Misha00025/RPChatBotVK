from Arkadia import Arkadia
from config import token

application = Arkadia(token=token, test_mode=True)

if __name__ == "__main__":
    application.start()