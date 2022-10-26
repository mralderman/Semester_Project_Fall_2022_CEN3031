from cryptography.fernet import Fernet

class user:
    def __init__(self, id, pas):
        self.fernet = Fernet(Fernet.generate_key())
        self.id = self.fernet.encrypt(id.encode())
        self.pas = self.fernet.encrypt(pas.encode())

    def check(self, id, pas):
        if self.fernet.decrypt(self.id).decode() == id and self.fernet.decrypt(self.pas).decode() == pas:
            print ("Login success!")
        else:
            print("Login failed!")

userList = {"admin": user("admin", "admin")}

def printLogin():
    print("1. Log in")
    print("2. Create New User")
    return input("Please select on of the options: ")

while True:
    match printLogin():
        case '1':
            print()
            print("Log in")
            userID = input("Enter Login ID:")
            userList[userID].check(userID, input("Enter password: "))
            break
        case '2':
            print()
            print("Create New User")
            userID = input("Enter Login ID:")
            userList[userID] = user(userID, input("Enter password: "))
        case other:
            print()
            print("Error, please try again")