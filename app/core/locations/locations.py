

class Location:
    def __init__(self):
        self._persons = []

    def add_person(self, person_id: str):
        if person_id not in self._persons:
            self._persons.append(person_id)

    def remove_person(self, person_id: str):
        self._persons.remove(person_id)

    def get_persons(self):
        return self._persons.copy()

    @property
    def persons_count(self):
        return len(self._persons)

