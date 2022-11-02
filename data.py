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
        next(reader)
        for row in reader:
            users.update({row[0] : User(row[1], row[2])})
    file.close()

def get_activities_from_file():
    
    with open('data.csv') as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            users[row[0]].activities.append(row[1],float(row[2]),float(row[3]))
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

get_users_from_file()

for i in users:
    print(i, " ", users[i].pas)






"""
def check_similar_users(users, value):
    for user in users:
        if user == value:
            return False
    return True



with open('data.csv') as file:
    reader = csv.reader(file, delimiter=',')
    next(reader)
    for row in reader:
        data_values.append(User(row[0], row[1], int(row[2]), int(row[3])))
        if check_similar_users(users, row[0]):
            users.append(row[0])
    
file.close()

for i in data_values:
    print(i.user_id + " " + i.activity + " ", i.unitAmount, " ", i.total)
for j in users:
    print(j)
"""
