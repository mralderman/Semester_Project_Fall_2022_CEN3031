from cryptography.fernet import Fernet
import data


def login(user_id, pas):
    key = data.users[user_id].key
    decrypted_pass = key.decrypt(data.users[user_id].get_user_pas()).decode()
    if (data.users[user_id].get_user_pas() is not None) & (decrypted_pass == pas):
        return True
    else:
        return False


def new_user(user_id, pas):
    key = Fernet(Fernet.generate_key())
    data.new_user(user_id, key.encrypt(pas.encode()), key)
