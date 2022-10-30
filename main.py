from cryptography.fernet import Fernet


class User:
    def __init__(self, user_id, pas):
        self.fernet = Fernet(Fernet.generate_key())
        self.id = self.fernet.encrypt(user_id.encode())
        self.pas = self.fernet.encrypt(pas.encode())

    def check(self, user_id, pas):
        if self.fernet.decrypt(self.id).decode() == user_id and self.fernet.decrypt(self.pas).decode() == pas:
            print("Login success!")
        else:
            print("Login failed!")


def print_login():
    print("1. Log in")
    print("2. Create New User")
    return input("Please select on of the options: ")


def authentication_prototype():
    user_list = {"admin": User("admin", "admin")}

    while True:
        match print_login():
            case '1':
                print()
                print("Log in")
                user_id = input("Enter Login ID:")
                user_list[user_id].check(user_id, input("Enter password: "))
                break
            case '2':
                print()
                print("Create New User")
                user_id = input("Enter Login ID:")
                user_list[user_id] = User(user_id, input("Enter password: "))
            case _:
                print()
                print("Error, please try again")
