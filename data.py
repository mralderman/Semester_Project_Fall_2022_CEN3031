import csv

class User:
    def __init__(self, pas, key):
        self.pas = pas
        self.key = key
        self.activities = []

    def get_user_pas(self):
        return self.pas

    def add_activity(self, user_id, name, rate, amount):
        self.activities.append(Activity(name, rate, amount))
        with open('data.csv', 'a', newline='') as file:
            append_object = csv.writer(file)
            appender = [user_id,name,rate,amount]
            append_object.writerow(appender)
        file.close()

class Activity:
    def __init__(self, name, rate, amount):
        self.name = name
        self.rate = rate
        self.amount = amount
        self.total = rate * amount


users = dict({'test': User("test", 1)})
events = {
    "Meatless meal" : [6.0, "kg/meal"],
    "Compost" : [1.7, "kg/lbf"],
    "Recycle" : [0.33, "kg/lbf"],
    "Install LED bulb" : [0.38, "kg/bulb"],
    "Take a 5 minute cold shower" : [0.2, "kg/shower"],
    "Turn AC off" : [0.4, "kg/hr"],
    "Plant a tree" : [10.0, "kg/tree"],
    "Pick up trash" : [0.33, "kg/lbf"],
    "Travel by bike" : [0.4, "kg/lbf"],
    "Carpool" : [0.2, "kg/mile"],
    "Reusable water bottle" : [0.01, "kg/fl. oz"],
    "Buy second hand clothing" : [0.01, "kg/item"],
    "Reusable shopping bag" : [1.6, "kg/bag"],
}

def new_user(user_id, pas, key):
    users[user_id] = User(pas, key)
    with open('user_pass.csv', 'a', newline='') as file:
        append_object = csv.writer(file)
        appender = [user_id,pas,key]
        append_object.writerow(appender)
    file.close()

def get_users_from_file(): # use this function first to make the dictionary of user names
    
    with open('user_pass.csv') as file:
        reader = csv.reader(file, delimiter=',')
        
        for row in reader:
            users.update({row[0] : User(row[1], row[2])})
    file.close()

def get_activities_from_file():
    
    with open('data.csv') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            users[row[0]].activities.append(Activity(row[1],float(row[2]),float(row[3])))
    file.close()


# Please Fix
# CSV should be as follows:
# num of users
# list users' user_ids, pas, key
# list of activites: user_id, name (of activity), rate, amount

# things I need to make
# 1. write data to file x
# 2. read from file and add to user's activity's list at the beginning x
# 3. read from users file and create a list of users x


