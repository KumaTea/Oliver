import os
import json


files = []
vote_data = {}
path = '.'

for i in os.listdir(path):
    if os.path.isfile(f'{path}/{i}'):
        files.append(f'{path}/{i}')
if files:
    for i in files:
        with open(i, 'r') as f:
            vote_data[i[2:]] = json.load(f)

with open('vote.json', 'w') as f:
    json.dump(vote_data, f)
