from cryptography.fernet import Fernet
import data
from enum import Enum


class NewUserOptions(Enum):
    USER_CREATED = 0
    USER_EXISTS = 1
    PAS_MISMATCH = 2
    BLANK_USER = 3


# Compares submitted username and password to stored usernames and passwords to validate login
def login(user_id: str, pas: str) -> bool: 
    try:
        key = Fernet(data.users[user_id].key)
        decrypted_pass = key.decrypt(data.users[user_id].get_user_pas()).decode()
        if (data.users[user_id].get_user_pas() is not None) & (decrypted_pass == pas):
            return True
        else:
            return False
    except:
        return False


# Creates a new user and encrypts their password
def new_user(user_id: str, pas: str, pas_conf: str) -> NewUserOptions:
    if data.users.get(user_id):
        return NewUserOptions.USER_EXISTS

    if pas != pas_conf:
        return NewUserOptions.PAS_MISMATCH
 
    if user_id == '' or user_id == ' ':
        return NewUserOptions.BLANK_USER
        
    key = Fernet.generate_key()  # separate key into key and token send key into new user not token
    cypher = Fernet(key)
    data.new_user(user_id, cypher.encrypt(pas.encode()), key)
    return NewUserOptions.USER_CREATED
