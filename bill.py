import models

class Bill(models.BasicModel):
    _FIELDS_MAPPING = {
        'billID': int,
        'date': str,
        'deadline': str,
        'sum': int,
        'description': str,
        'student': int,
        'client': int,
        'category': int,
        'status': str,
        'views': int,
        'executors': str   
    }
    _TABLE= 'bills'
    def __init__(self):
        self._FIELDS_MAPPING['date'] = ''
        self._FIELDS_MAPPING['deadline'] = ''
        self._FIELDS_MAPPING['sum'] = 0
        self._FIELDS_MAPPING['description'] = ''
        self._FIELDS_MAPPING['student'] = ''
        self._FIELDS_MAPPING['client'] = ''
        self._FIELDS_MAPPING['category'] = ''
        self._FIELDS_MAPPING['status'] = ''
        self._FIELDS_MAPPING['views'] = 0
        self._FIELDS_MAPPING['executors'] = ''

        
    def _create_DB(self):
        """
        Здесь мы проверяем существование таблицы
        Если нет - создаем и накатываем поля
        """
        self.query("""
                CREATE TABLE IF NOT EXISTS bills 
                (
                    `billID` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    `date` TEXT,
                    `deadline` TEXT,
                    `sum` INTEGER,
                    `description` TEXT,
                    `student` INTEGER,
                    `client` INTEGER,
                    `category` INTEGER,
                    `status` TEXT,
					`views` INTEGER,
					`executors`, TEXT
					
                )
            """)
    def _create_mapping(self):
        self._create_DB()

        array = (list(self._FIELDS_MAPPING.values())[1:])
        self.query_param(
            """
                INSERT INTO bills (date, deadline, sum, description, student, client, category, status, views, executors) VALUES(?,?,?,?,?,?,?,?,?,?)
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
                UPDATE bills
                SET
                    date =?,
                    deadline =?,
                    sum=?,
                    description=?,
                    student=?,
                    client=?,
                    category=?,
                    status=?,
					views=?,
					executors=?
                WHERE billID = ?
            """, arr)
b=Bill()
print(b.to_dict())