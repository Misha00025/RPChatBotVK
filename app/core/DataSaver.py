import os.path
import pickle


_save_dir = "saves"


def _get_path(name):
    return os.path.join(_save_dir, name+".pkl")


def save(obj, name):
    if not os.path.exists(_save_dir):
        os.makedirs(_save_dir)
    _save_file = _get_path(name)
    with open(_save_file, "wb") as file:
        pickle.dump(obj, file)


def load(name):
    try:
        with open(_get_path(name), "rb") as file:
            res = pickle.load(file)
        return 0, res
    except:
        print(f"Error on load file ({_get_path(name)})")
        return 1, None

