import random
import string
from datetime import datetime
import hashlib, uuid

def generate_token():
    _str = randomString(30)
    seconds = datetime.today().timestamp()
    return _str + str(seconds)

def randomString(stringLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

def get_hash_password(password):
    salt = 'e8cf8ab5f50e43a1156cf63e704c84608bb95bb5f435'
    hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    return hashed_password

def check_hash_password(password, hash):
    salt = 'e8cf8ab5f50e43a1156cf63e704c84608bb95bb5f435'
    hashed_password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    return hashed_password == hash