import csv

class Data:
    def __init__(self,uName,activity,unitAmount,total):
        self.uName = uName
        self.activity = activity
        self.unitAmount = unitAmount
        self.total = total

data_values = []
users = []
def check_similar_users(users, value):
    for user in users:
        if user == value:
            return False
    return True
with open('data.csv') as file:
    reader = csv.reader(file, delimiter=',')
    next(reader)
    for row in reader:
        data_values.append(Data(row[0],row[1],int(row[2]),int(row[3])))
        if check_similar_users(users, row[0]):
            users.append(row[0])
    
file.close()

for i in data_values:
    print(i.uName + " " + i.activity + " ", i.unitAmount, " ",i.total)
for j in users:
    print(j)

