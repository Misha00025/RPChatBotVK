from app.core.DataSaver import save, load
from .locations import Location


_locations: {str: Location} = {}
_user_location = {}
_save_name = "locations"
_is_loaded = False


def add_user(location_name, user_id):
    if location_name not in _locations.keys():
        _locations[location_name] = Location()
    user_id = str(user_id)
    location = _locations[location_name]
    location.add_person(user_id)
    # add user cache
    if user_id in _user_location.keys():
        remove_user(_user_location[user_id], user_id)
    _user_location[user_id] = location_name
    save_locations()
    # for key in _locations.keys():
    #     print(f"{key}:{_locations[key].get_persons()}")
    # print(_user_location)


def remove_user(location, user_id):
    if location in _locations.keys():
        _locations[location].remove_person(user_id)
    if user_id in _user_location.keys():
        _user_location[user_id] = None
    save_locations()


def get_user_location(user_id):
    if user_id not in _user_location.keys():
        return None
    return _user_location[user_id]


def get_users(location_name):
    if location_name not in _locations.keys():
        return None
    return _locations[location_name].get_persons()


def save_locations():
    save((_locations, _user_location), _save_name)


def load_locations():
    global _is_loaded, _locations, _user_location
    _is_loaded = True
    err, res = load(_save_name)
    if not err:
        _locations, _user_location = res


load_locations()
