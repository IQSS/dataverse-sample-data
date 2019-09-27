#from pyDataverse.api import Api
import json
import dvconfig
import os
import time
import csv
#import requests
from io import StringIO
base_url = dvconfig.base_url
api_token = dvconfig.api_token
paths = dvconfig.sample_data
#api = Api(base_url, api_token)
#print(api.status)
# TODO limit amount of recursion
#def check_dataset_lock(dataset_dbid):
#    query_str = '/datasets/' + str(dataset_dbid) + '/locks'
#    params = {}
#    resp = api.get_request(query_str, params=params, auth=True)
#    locks = resp.json()['data']
#    if (locks):
#        #print('Lock found for dataset id ' + str(dataset_dbid) + '... sleeping...')
#        time.sleep(2)
#        check_dataset_lock(dataset_dbid)
#resp = api.get_dataverse(':root')
#buff = StringIO("")
#if (resp.status_code == 401):
#if (True):
#    print('Publishing root dataverse.')
#    #resp = api.publish_dataverse(':root')
    #print(resp)
alldata = []
for path in paths:
    parts = path.split('/')
    json_file = parts[-1]
    dvtype = parts[-3]
    #print('dvtype', dvtype)
    if 'dataverses' == dvtype:
        dvtype = 'dataverse'
    else:
        dvtype = 'dataset'
    parent = parts[-4]
    if 'data' == parent:
        parent = ':root'
    if ('dataverse' == dvtype):
        pass
        #print('Creating ' + dvtype + ' ' + json_file + ' in dataverse ' + parent)
        ##dv_json = path
        ##with open(dv_json) as f:
        ##    #metadata = json.load(f)
        ##    dvmetadata = json.load(f)
        #print(metadata)
        # FIXME: Why is "identifier" required?
        #####identifier = metadata['alias']
        #resp = api.create_dataverse(identifier, json.dumps(metadata), parent=parent)
        #print(resp)
        #resp = api.publish_dataverse(identifier)
        #print(resp)
    else:
#        print('Creating ' + dvtype + ' ' + json_file + ' in dataverse ' + parent)
        dataset_json = path
        with open(dataset_json) as f:
            metadata = json.load(f)
        dataverse = parent
        #resp = api.create_dataset(dataverse, json.dumps(metadata))
        #print(resp)
        #dataset_pid = resp.json()['data']['persistentId']
        #dataset_dbid = resp.json()['data']['id']
        files_dir = path.replace(json_file, '') + 'files'
        #print(files_dir)
        for path,subdir,files in os.walk(files_dir):
           for name in files:
#                print('name', name)
                datarow = []
                #datarow.append(name[:20])
                datarow.append(name)
                #title = metadata['datasetVersion']['metadataBlocks']
                title = metadata['datasetVersion']['metadataBlocks']['citation']['fields'][0]['value']
                #print(title)
                subjects = metadata['datasetVersion']['metadataBlocks']['citation']['fields'][4]['value']
                if title == 'Reproductive Health Laws Around the World':
                    subjects = metadata['datasetVersion']['metadataBlocks']['citation']['fields'][5]['value']
                #datarow.append('FIXME')
                datarow.append(title)
                filepath = os.path.join(path,name)
                parts = filepath.split('/dataverses/')
                #datarow.append(parts)
                #alias1 = filepath[3]
                #alias1 = filepath.split('/')[2]
                alias1 = None
                name1 = None
                #dvname = dvmetadata['name']
                #name1 = 'FIXMENAME1'
                try:
                    alias1 = parts[1].split('/')[0]
                    dv_json = 'data/dataverses/' + alias1 + '/' + alias1 + '.json'
                    with open(dv_json) as f:
                        alias1md = json.load(f)
                    name1 = alias1md['name']
                except:
                    pass
                #alias1 = 'FIXMEALIAS1'
                datarow.append(alias1)
                datarow.append(name1)
                #alias2 = filepath.split('/')[4]
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
                #alias3 = filepath.split('/')[7]
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
                #print(subjects)
                datarow.append(';'.join(subjects))
                #datarow.append(filepath)
                relpath = os.path.relpath(filepath,files_dir)
                # "directoryLabel" is used to populate "File Path"
                directoryLabel, filename = os.path.split(relpath)
                #resp = api.upload_file(dataset_pid, "'" + filepath + "'")
                #print(resp)
                #file_id = resp['data']['files'][0]['dataFile']['id']
                ## This lock check and sleep is here to prevent the dataset from being permanently
                ## locked because a tabular file was uploaded first.
                #check_dataset_lock(dataset_dbid)
                file_metadata = {}
                # TODO: Think more about where the description comes from. A "sidecar" file as proposed at https://github.com/IQSS/dataverse/issues/5924#issuecomment-499605672 ?
                #file_metadata['description'] = 'Sidecar?'
                file_metadata['directoryLabel'] = directoryLabel
                jsonData = json.dumps(file_metadata)
                data = { 'jsonData' : jsonData }
                headers = {
                    'X-Dataverse-key': api_token,
                }
                publication_date = '2019-09-27'
                datarow.append(publication_date)
                alldata.append(datarow)
                

for i in alldata:
    print
    print(i)
outfile = open('./files.tsv','w')
writer=csv.writer(outfile, delimiter='\t')
#writer.writerow(['SNo', 'States', 'Dist', 'Population'])
writer.writerow(['filename', 'dataset_name', 'dataverse_level_1_alias', 'dataverse_level_1_friendly', 'dataverse_level_2_alias', 'dataverse_level_2_friendly', 'dataverse_level_3_alias', 'dataverse_level_3_friendly', 'subjects', 'publication_date'])
#writer.writerows(list_of_rows)
writer.writerows(alldata)
#with open("output.tsv",'wb') as resultFile:
#outfile=open('./immates.csv','w')
#    wr = csv.writer(resultFile)
#    for i in datarow:
#        print(i)
#        wr.writerow(i + '')
                #resp = requests.post(base_url + '/api/files/' + str(file_id) + '/metadata', data=data, headers=headers, stream=True, files=buff)
                #print(resp)
        # Sleep a little more to avoid org.postgresql.util.PSQLException: ERROR: deadlock detected
        #time.sleep(2)
        #print('Publishing dataset id ' + str(dataset_dbid))
        # TODO: Switch to pyDataverse api.publish_dataset after this issue is fixed: https://github.com/AUSSDA/pyDataverse/issues/24
        #resp = requests.post(base_url + '/api/datasets/' + str(dataset_dbid) + '/actions/:publish?type=major&key=' + api_token)
        #print(resp)