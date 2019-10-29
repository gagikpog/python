from models import  BasicModel

class Token(BasicModel):
    # def get_user_by_token(self, token):
    _FIELDS_MAPPING = {
        'token': str,
        'userID': int,
        'date': str
    }
    _TABLE = 'token'
    _PRIMARY_KEY = 'token'
    def __init__(self):
        self._FIELDS_MAPPING['token'] = ''
        self._FIELDS_MAPPING['userID'] = 0
        self._FIELDS_MAPPING['date'] = ''

    def _create_DB(self):
        self.query("""
                CREATE TABLE IF NOT EXISTS token
                (
                    `token` TEXT PRIMARY KEY UNIQUE,
                    `userID` INTEGER,
                    `date` TEXT
                )
            """)

    def create_token(self):
        self._create_DB()

        arr = (list(self._FIELDS_MAPPING.values()))
        self.query(
            """
                INSERT INTO token (
                    token,
                    userID,
                    date
                ) VALUES(?,?,?)
            """, arr)
    
    def delete_token(self, token):
        self.query(
            """
                DELETE FROM token WHERE token=?
            """, token)