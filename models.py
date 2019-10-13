import sqlite3

class ValidationError(Exception):
    """Ошибка валидации"""

class SQLModel:
    _DATABASE = None
    _TABLE = None

    @classmethod
    def _connect(cls):
        return sqlite3.connect(cls._DATABASE)

    @classmethod
    def query(cls, query):
        conn = cls._connect()
        cur = conn.cursor()

        cur.execute(query)
        conn.commit()
        conn.close()

    @classmethod
    def query_param(cls, query, param):
        conn = cls._connect()
        cur = conn.cursor()

        cur.execute(query, param)
        conn.commit()
        conn.close()

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
                    `activity` TEXT
                )
            """)

    def _create_mapping(self):
        self._create_DB()

        arr = (list(self._FIELDS_MAPPING.values())[1:])
        self.query_param(
            """
                INSERT INTO user (name, sname, pname, born, phone, rating, mail, activity) VALUES(?,?,?,?,?,?,?,?)
            """, arr)

    def _update_mapping(self):
        """
        Здесь мы проверяем что у нас есть в бд из полей
        Если чего то нет - досоздаем
        """
        self._create_DB()
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
                    activity=?
                WHERE userID = ?
            """, arr)

    @classmethod
    def _get_by_pk(cls, pk):
        conn = cls._connect()
        cur = conn.cursor()

        cur.execute(
            """
                SELECT *
                FROM :table
                WHERE userID = :id
            """.replace(':table', cls._TABLE).replace(':id', str(pk))
        )

        result = {}
        record = cur.fetchone()
        for idx, col in enumerate(cur.description):
            result[col] = record[idx]
        conn.close()
        return result

    def get_by_pk(self, pk):
        record = self._get_by_pk(pk)
        self._create_DB()

        self.fill_data(record)
        return self
        # return record

class BasicModel(SQLModel):
    # Поля модели
    _FIELDS_MAPPING = {}
    _INNER_DATA = {}
    _DATABASE = 'studer.db'

    def __getattr__(self, attr):
        if attr in self._FIELDS_MAPPING.keys():
            return self._FIELDS_MAPPING[attr]
        raise AttributeError()

    def __setattr__(self, attr, value):
      if attr in self._FIELDS_MAPPING.keys():
          self._FIELDS_MAPPING[attr] = value

    def fill_data(self, data):
        """
        Args:
            data (dict): данные модели
        """
        for key, val in data.items():
            if self._validate(key, val):
                self.__dict__[key] = val

    def _validate(self, key, val):
        key_type = self._FIELDS_MAPPING.get(key)
        if not key_type:
            return False
        if key_type != type(val):
            raise ValidationError
        return True

    def to_dict(self):
        inner_dict ={}
        for key in self._FIELDS_MAPPING:
            inner_dict[key] = getattr(self, key)
        return inner_dict
