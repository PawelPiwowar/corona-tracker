import json

with open('pobrane.json', 'r') as json_file:
    data = json.load(json_file)

data2 = []

for el in data:
    if el['country'] == 'Poland' or el['country'] == 'Ukraine':
        data2.append(el)

with open('ECDC-short.json', 'w') as outfile:
    json.dump(data2, outfile)



