import json
import dvconfig
import os
import time
import csv
from io import StringIO
base_url = dvconfig.base_url
api_token = dvconfig.api_token
paths = dvconfig.sample_data
alldata = []
for path in paths:
    parts = path.split('/')
    json_file = parts[-1]
    dvtype = parts[-3]
    if 'dataverses' == dvtype:
        dvtype = 'dataverse'
    else:
        dvtype = 'dataset'
    parent = parts[-4]
    if 'data' == parent:
        parent = ':root'
    if ('dataverse' == dvtype):
        pass
    else:
        dataset_json = path
        with open(dataset_json) as f:
            metadata = json.load(f)
        dataverse = parent
        files_dir = path.replace(json_file, '') + 'files'
        for path,subdir,files in os.walk(files_dir):
           for name in files:
                datarow = []
                datarow.append(name)
                title = metadata['datasetVersion']['metadataBlocks']['citation']['fields'][0]['value']
                subjects = metadata['datasetVersion']['metadataBlocks']['citation']['fields'][4]['value']
                # FIXME: clean up this special case
                if title == 'Reproductive Health Laws Around the World':
                    subjects = metadata['datasetVersion']['metadataBlocks']['citation']['fields'][5]['value']
                datarow.append(title)
                filepath = os.path.join(path,name)
                parts = filepath.split('/dataverses/')
                alias1 = None
                name1 = None
                try:
                    alias1 = parts[1].split('/')[0]
                    dv_json = 'data/dataverses/' + alias1 + '/' + alias1 + '.json'
                    with open(dv_json) as f:
                        alias1md = json.load(f)
                    name1 = alias1md['name']
                except:
                    pass
                datarow.append(alias1)
                datarow.append(name1)
                alias2 = None
                name2 = None
                try:
                    alias2 = parts[2].split('/')[0]
                    dv_json = 'data/dataverses/' + alias1 + '/dataverses/' + alias2 + '/' + alias2 + '.json'
                    with open(dv_json) as f:
                        alias2md = json.load(f)
                    name2 = alias2md['name']
                except:
                    pass
                datarow.append(alias2)
                datarow.append(name2)
                alias3 = None
                name3 = None
                try:
                    alias3 = parts[3].split('/')[0]
                    dv_json = 'data/dataverses/' + alias1 + '/dataverses/' + alias2 + '/dataverses/' + alias3 + '/' + alias3 + '.json'
                    with open(dv_json) as f:
                        alias2md = json.load(f)
                    name2 = alias2md['name']
                except:
                    pass
                datarow.append(alias3)
                datarow.append(name3)
                datarow.append(';'.join(subjects))
                # TODO: stop hard coding date
                publication_date = '2019-09-27'
                datarow.append(publication_date)
                alldata.append(datarow)
                

for i in alldata:
    print
    print(i)
outfile = open('./files.tsv','w')
writer=csv.writer(outfile, delimiter='\t')
writer.writerow(['filename', 'dataset_name', 'dataverse_level_1_alias', 'dataverse_level_1_friendly', 'dataverse_level_2_alias', 'dataverse_level_2_friendly', 'dataverse_level_3_alias', 'dataverse_level_3_friendly', 'subjects', 'publication_date'])
writer.writerows(alldata)
