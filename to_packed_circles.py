import csv
import json
from collections import defaultdict
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
data = defaultdict(dict)
#data['name'] = 'root'
#data['children'] = []
seen = defaultdict(dict)
with open('files.tsv', newline='') as tsvfile:
    reader = csv.DictReader(tsvfile, delimiter="\t")
    rows = [row for row in reader]
    for row in rows:
        filename = row['filename']
        dv1name = row['dataverse_level_1_friendly']
        dv2name = row['dataverse_level_2_friendly']
        dv3name = row['dataverse_level_3_friendly']
        title = row['dataset_name']
        #print("%-20s > %-20s > %-20s > %-20s > %-20s" % (dv1name[:20], dv2name[:20], dv3name[:20], title[:20], filename[:20]))
        if dv3name:
            if seen[dv1name + dv2name + dv3name + title]:
                data[dv1name][dv2name][dv3name][title] += 1
            else:
                if not data[dv1name].get(dv2name):
                    data[dv1name][dv2name] = {}
                if not data[dv1name].get(dv2name).get(dv3name):
                    data[dv1name][dv2name][dv3name] = {}
                data[dv1name][dv2name][dv3name] = {}
                data[dv1name][dv2name][dv3name][title] = 1
                seen[dv1name + dv2name + dv3name + title] = 1
        elif dv2name:
            if seen[dv1name + dv2name + title]:
                data[dv1name][dv2name][title] += 1
            else:
                if not data[dv1name].get(dv2name):
                    data[dv1name][dv2name] = {}
                data[dv1name][dv2name][title] = 1
                seen[dv1name + dv2name + title] = 1
        else:
            if seen[dv1name + title]:
                data[dv1name][title] += 1
            else:
                data[dv1name][title] = 1
                seen[dv1name + title] = 1
out = json.dumps(data, indent=2)
print(out)
