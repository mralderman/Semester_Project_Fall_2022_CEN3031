import csv

class Activity:
    
    def __init__(self, name: str, rate: float, amount: float):
        self.name: str = name
        self.rate: float = rate
        self.amount: float = amount
        self.total: float = rate * amount

class User:
    
    def __init__(self, pas, key, activities = None) -> None:
        self.pas: str = pas
        self.key: str = key
        if activities is None:
           activities: list = []
        self.activities: list = activities 
        self.grand_total: float = 0.0
        self.custom_activities: dict[str, tuple] = {}
        self.private: bool = False

    def get_user_pas(self) -> str:
        return self.pas
    

    def add_activity(self, user_id: str, name: str, rate: float, amount: float) -> None:
        self.activities.append(Activity(name, rate, amount))
        self.grand_total: float = self.grand_total + (rate * amount)
        with open('data.csv', 'a', newline='') as file:
            append_object = csv.writer(file)
            appender = [user_id, name, rate, amount]
            append_object.writerow(appender)
        file.close()
    
    def get_user_activities(self):
        return self.activities
    
    def privacy_on(self) -> None:
        self.private = True

    def privacy_off(self) -> None:
        self.private = False 



users: dict[str, User] = {}

def getUser(userId: str) -> None:
    return users[userId]


activities_templates: dict[str, tuple] = {
    "Meatless meal" : (6.0, "kg/meal"),
    "Compost" : (1.7, "kg/lbf"),
    "Recycle" : (0.33, "kg/lbf"),
    "Install LED bulb" : (0.38, "kg/bulb"),
    "Take a 5 minute cold shower" : (0.2, "kg/shower"),
    "Turn AC off" : (0.4, "kg/hr"),
    "Plant a tree" : (10.0, "kg/tree"),
    "Pick up trash" : (0.33, "kg/lbf"),
    "Travel by bike" : (0.4, "kg/lbf"),
    "Carpool" : (0.2, "kg/mile"),
    "Reusable water bottle" : (0.01, "kg/fl. oz"),
    "Buy second hand clothing" : (0.01, "kg/item"),
    "Reusable shopping bag" : (1.6, "kg/bag"),
}


def load_custom_activity_templates():
    with open('custom_activities.csv') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            if row[0] in users.keys():
                users[row[0]].custom_activities[row[1]] = (row[2], 'kg/unit')
    file.close()


def create_custom_activity_template(user_id: str,name: str, rate: int):
    users[user_id].custom_activities[name] = (rate, 'kg/unit')
    with open('custom_activities.csv', 'a', newline='') as file:
        append_object = csv.writer(file)
        appender = [user_id, name, rate]
        append_object.writerow(appender)
    file.close()


def new_user(user_id: str, pas, key) -> None:
    users[user_id] = User(pas, key)
    res: bytes = user_id.encode('utf-8')
    spacer = '\n'
    spacer_ab = spacer.encode('utf-8')
    with open('user_pass.txt', 'ab') as file:
        file.write(res)
        file.write(spacer_ab)
        file.write(pas)
        file.write(spacer_ab)
        file.write(key)
        file.write(spacer_ab)
    file.close()


def get_users_from_file() -> None:  # use this function first to make the dictionary of user names
    my_file = open("user_pass.txt", "rb")
    my_line = my_file.readline()
    while my_line:
        idb = my_line.rstrip(b'\n')
        use_id = idb.decode()
        sec = my_file.readline()
        password = sec.rstrip(b'\n')
        third = my_file.readline()
        the_key = third.rstrip(b'\n')
        my_line = my_file.readline()
        users.update({use_id : User(password, the_key)})
    my_file.close()


def get_activities_from_file() -> None:
    
    with open('data.csv') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            if row[0] in users.keys():
                users[row[0]].activities.append(Activity(row[1], float(row[2]), float(row[3])))
                users[row[0]].grand_total = users[row[0]].grand_total + (float(row[2]) * float(row[3]))
    file.close()

