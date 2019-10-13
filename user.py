import models

class User(models.BasicModel):
    _FIELDS_MAPPING = {
        'userID': int,
        'name': str,
        'sname': str,
        'pname': str,
        'born': str,
        'phone': str,
        'rating': int,
        'mail': str,
        'activity': str
    }
    _TABLE = 'user'
    def __init__(self):
        self._FIELDS_MAPPING['userID'] = 1
        self._FIELDS_MAPPING['name'] = 'name'
        self._FIELDS_MAPPING['sname'] = 'sname'
        self._FIELDS_MAPPING['pname'] = 'pname'
        self._FIELDS_MAPPING['born'] = 'born'
        self._FIELDS_MAPPING['phone'] = 'phone'
        self._FIELDS_MAPPING['rating'] = 1
        self._FIELDS_MAPPING['mail'] = 'mail'
        self._FIELDS_MAPPING['activity'] = 'activity'
        pass

        
a = User()
a.get_by_pk(1)

# print(a.__dict__)
# print(a)
