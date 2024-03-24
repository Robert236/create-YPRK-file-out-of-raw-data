import json
import csv

new_data = []
print_data = []

Startdatum = '20.03.2024'
Enddatum = '31.12.9999'
hierarchy_number = None

with open('Rohdaten in neues Format.csv', 'r') as InputFile:
    header = None
    for i, line in enumerate(InputFile):
        if i == 1:
            line = line.replace('\n', '')
            hierarchy_number = line.split(';')[8]
        elif i == 5:
            line = line.replace('\n', '')
            header = line.split(';')
        elif i > 5:
            line = line.replace('\n', '')
            data = line.split(';')
            if data[2]:
                rv = dict(zip(header, data))
                new_data.append(rv)


last_dataset = None
for i, line2 in enumerate(new_data):
    without_EUR = line2['Preis neu'].replace(' €', '')
    line2['Preis neu'] = without_EUR
    if i == 0:
        line2['Zähler'] = 1
        last_dataset = line2
    else:
        if line2['Materialnummer REIFF'] == last_dataset['Materialnummer REIFF']:
            line2['Zähler'] = last_dataset['Zähler'] + 3
            last_dataset = line2
        else:
            line2['Zähler'] = 1
            last_dataset = line2


for line3 in new_data:
    template = open('template.json', 'r')
    template = json.load(template)
    template['E'] = hierarchy_number
    template['G'] = line3['Materialnummer REIFF']
    template['AG'] = line3['Zähler']
    template['AI'] = line3['Staffelmenge']
    template['AJ'] = line3['ME']
    template['AM'] = line3['Preis neu']
    template['AO'] = line3['per']
    template['AP'] = line3['ME']
    template['AQ'] = Startdatum
    template['AR'] = Enddatum
    print_data.append(template)


with open('YPRK_File.csv', 'w') as csvfile:
    fieldnames = []
    template = open('template.json', 'r')
    template = json.load(template)
    for key, value in template.items():
        fieldnames.append(key)
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    for dataset in print_data:
        writer.writerow(dataset)
