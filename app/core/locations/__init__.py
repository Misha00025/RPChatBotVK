from .locations import Location


_locations: {str: Location} = {}
_user_location = {}


def add_user(location_name, user_id):
    if location_name not in _locations.keys():
        _locations[location_name] = Location()
    location = _locations[location_name]
    location.add_person(user_id)
    # add user cache
    if user_id in _user_location.keys():
        remove_user(_user_location[user_id], user_id)
    _user_location[user_id] = location_name
    print(_locations)
    print(_user_location)


def remove_user(location, user_id):
    if location in _locations.keys():
        _locations[location].remove_person(user_id)
    if user_id in _user_location.keys():
        _user_location[user_id] = None


def get_user_location(user_id):
    if user_id not in _user_location.keys():
        return None
    return _user_location[user_id]


def get_users(location_name):
    if location_name not in _locations.keys():
        return None
    return _locations[location_name].get_persons()
