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
        'activity': str,
        'studID': int
    }

    _TABLE = 'user'
    _PRIMARY_KEY = 'userID'

    def __init__(self):
        self._FIELDS_MAPPING['name'] = ''
        self._FIELDS_MAPPING['sname'] = ''
        self._FIELDS_MAPPING['pname'] = ''
        self._FIELDS_MAPPING['born'] = ''
        self._FIELDS_MAPPING['phone'] = ''
        self._FIELDS_MAPPING['rating'] = 0
        self._FIELDS_MAPPING['mail'] = ''
        self._FIELDS_MAPPING['activity'] = ''
        self._FIELDS_MAPPING['studID'] = 0
        pass

    def _create_DB(self):
        """
        Здесь мы проверяем существование таблицы
        Если нет - создаем и накатываем поля
        """
        self.query("""
                CREATE TABLE IF NOT EXISTS user
                (
                    `userID` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    `name` TEXT,
                    `sname` TEXT,
                    `pname` TEXT,
                    `born` TEXT,
                    `phone` TEXT,
                    `rating` INTEGER,
                    `mail` TEXT,
                    `activity` TEXT,
                    `studID` INTEGER
                )
            """)

    def _create_mapping(self):
        self._create_DB()

        arr = (list(self._FIELDS_MAPPING.values())[1:])
        self.query(
            """
                INSERT INTO user (
                    name,
                    sname,
                    pname,
                    born,
                    phone,
                    rating,
                    mail,
                    activity,
                    studID
                ) VALUES(?,?,?,?,?,?,?,?,?)
            """, arr)

    def _update_mapping(self):
        """
        Здесь мы проверяем что у нас есть в бд из полей
        Если чего то нет - досоздаем
        """
        _list = list(self._FIELDS_MAPPING.values())
        arr = (_list[1:])
        arr.append(_list[0])
        self.query(
            """
                UPDATE user
                SET
                    name =?,
                    sname =?,
                    pname=?,
                    born=?,
                    phone=?,
                    rating=?,
                    mail=?,
                    activity=?,
                    studID=?
                WHERE userID = ?
            """, arr)
