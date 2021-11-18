import json

with open('users.json', 'r') as file:
	fl = json.load(file)

with open('users_list.json', 'r') as dile:
	us_list = json.load(dile)


for i in range(len(fl['Users'])):
	fl['Users'][(us_list['Users_list'][i])]['notification'] = 0


with open('users.json', 'w') as file:
	json.dump(fl, file, indent = 4)
#print(fl)	