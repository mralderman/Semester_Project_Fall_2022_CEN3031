import csv


class User:
    def __init__(self, pas, key):
        self.pas = pas
        self.key = key
        self.activities = []

    def get_user_pas(self):
        return self.pas

    def add_activity(self, name, rate, amount):
        self.activities.append(Activity(name, rate, amount))


class Activity:
    def __init__(self, name, rate, amount):
        self.name = name
        self.rate = rate
        self.amount = amount
        self.total = rate * amount


users = dict({'test': User("test", 1)})


def new_user(user_id, pas, key):
    users[user_id] = User(pas, key)

# Please Fix
# CSV should be as follows:
# num of users
# list users' user_ids, pas, key
# list of activites: user_id, name (of activity), rate, amount

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
