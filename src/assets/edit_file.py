import json
from datetime import datetime

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

for el in dataFull:
    comparison_year = datetime.strptime('2020 50 0', "%Y %W %w")
    datetime = datetime.strptime(el['year_week'].replace('-', ' ') + ' 0', "%Y %W %w")
    if (el['indicator'] == 'cases') and (datetime > comparison_year):
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



