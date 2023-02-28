from Arkadia import Arkadia
from config import token



application = Arkadia(token=token)

if __name__ == "__main__":
    application.start()