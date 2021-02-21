import json

with open('pobrane.json', 'r') as json_file:
    data = json.load(json_file)

data2 = []

for el in data:
    if (el['country'] == 'Poland' or el['country'] == 'Ukraine') and (el['indicator'] == 'cases'):
        del el['country_code']
        del el['continent']
        del el['population']
        del el['indicator']
        del el['source']
        del el['cumulative_count']
        data2.append(el)

with open('ECDC-short.json', 'w') as outfile:
    json.dump(data2, outfile)


with open('pobrane.json', 'r') as json_file:
    dataFull = json.load(json_file)

dataFullFinished = []

for el in reversed(dataFull):
    if el['year_week'] == '202-50':
        break
    if el['indicator'] == 'cases':
        check = el.get('country_code', None)
        if check:
            del el['country_code']
        del el['continent']
        del el['population']
        del el['indicator']
        del el['source']
        del el['cumulative_count']
        dataFullFinished.append(el)

with open('ECDC-full.json', 'w') as outfile2:
    json.dump(dataFullFinished, outfile2)

print('finished')



