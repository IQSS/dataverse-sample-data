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
final = {}
final['name'] = 'root'
final['children'] = []
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
data_out = json.dumps(data, indent=2)
#print(data_out)
#for child_of_root in data:
# for key, value in ourNewDict.items():

# cor is "child of root"
for corkey, corval in data.items():
    #print(corkey)
    level1 = {}
    level1['name'] = corkey
    # gcor = "grandchild of root"
    for gcorkey, gcorval in corval.items():
        # ggcor = "great grandchild of root"
        if isinstance(gcorval,dict):
        #if gcorval.items():
            for ggcorkey, ggcorval in gcorval.items():
                #print('ggcorkey:', ggcorkey)
                level3 = {}
                level3['name'] = gcorkey
                level2['children'] = []
                level2['children'].append(level3)
        #print(gcorkey)
        level2 = {}
        level2['name'] = gcorkey
        level1['children'] = []
        level1['children'].append(level2)
    final['children'].append(level1)
final_out = json.dumps(final, indent=2)
print(final_out)
