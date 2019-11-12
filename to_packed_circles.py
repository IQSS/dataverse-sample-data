import csv
import json
'''
filename
dataset_name
dataverse_level_1_alias
dataverse_level_1_friendly
dataverse_level_2_alias
dataverse_level_2_friendly
dataverse_level_3_alias
dataverse_level_3_friendly
subjects
publication_date
'''
data = {}
data['name'] = 'root'
data['children'] = []
with open('files.tsv', newline='') as tsvfile:
    reader = csv.DictReader(tsvfile, delimiter="\t")
    rows = [row for row in reader]
    for row in rows:
        filename = row['filename']
        dv1name = row['dataverse_level_1_friendly']
        dv2name = row['dataverse_level_2_friendly']
        dv3name = row['dataverse_level_3_friendly']
        title = row['dataset_name']
out = json.dumps(data, indent=2)
print(out)
