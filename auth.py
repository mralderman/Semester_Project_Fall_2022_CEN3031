from cryptography.fernet import Fernet
import data
from enum import Enum


class NewUserOptions(Enum):
    USER_CREATED = 0
    USER_EXISTS = 1
    PAS_MISMATCH = 2


def login(user_id, pas):
    try:
        key = Fernet(data.users[user_id].key)
        decrypted_pass = key.decrypt(data.users[user_id].get_user_pas()).decode()
        print(decrypted_pass)
        if (data.users[user_id].get_user_pas() is not None) & (decrypted_pass == pas):
            return True
        else:
            return False
    except:
        return False


def new_user(user_id, pas, pas_conf):
    if data.users.get(user_id):
        return NewUserOptions.USER_EXISTS

    if pas != pas_conf:
        return NewUserOptions.PAS_MISMATCH
 # separate key into key and token send key into new user not token
    key = Fernet.generate_key()
    cypher = Fernet(key)
    data.new_user(user_id, cypher.encrypt(pas.encode()), key)
    return NewUserOptions.USER_CREATED
