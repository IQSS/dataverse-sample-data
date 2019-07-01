from pyDataverse.api import Api
import json
import dvconfig
import os
import time
import requests
base_url = dvconfig.base_url
api_token = dvconfig.api_token
paths = dvconfig.sample_data
api = Api(base_url, api_token)
print(api.status)
resp = api.get_dataverse(':root')
if (resp.status_code == 401):
    print('Publishing root dataverse.')
    resp = api.publish_dataverse(':root')
    print(resp)
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
        print('Creating ' + dvtype + ' ' + json_file + ' in dataverse ' + parent)
        dv_json = path
        with open(dv_json) as f:
            metadata = json.load(f)
        print(metadata)
        # FIXME: Why is "identifier" required?
        identifier = metadata['alias']
        resp = api.create_dataverse(identifier, json.dumps(metadata), parent=parent)
        print(resp)
        resp = api.publish_dataverse(identifier)
        print(resp)
    else:
        print('Creating ' + dvtype + ' ' + json_file + ' in dataverse ' + parent)
        dataset_json = path
        with open(dataset_json) as f:
            metadata = json.load(f)
        dataverse = parent
        resp = api.create_dataset(dataverse, json.dumps(metadata))
        print(resp)
        dataset_pid = resp.json()['data']['persistentId']
        dataset_dbid = resp.json()['data']['id']
        files_dir = path.replace(json_file, '') + 'files'
        print(files_dir)
        if not os.path.isdir(files_dir):
            pass
        else:
            # TODO: support file hierarchy
            for f in os.listdir(files_dir):
                datafile = files_dir + '/' + f
                print(datafile)
                resp = api.upload_file(dataset_pid, datafile)
                print(resp)
                # This sleep is here to prevent the dataset from being permanently
                # locked because a tabular file was uploaded first.
                time.sleep(3)
        # Sleep a little more to avoid org.postgresql.util.PSQLException: ERROR: deadlock detected
        time.sleep(2)
        print('Publishing dataset id ' + str(dataset_dbid))
        # TODO: Switch to pyDataverse api.publish_dataset after this issue is fixed: https://github.com/AUSSDA/pyDataverse/issues/24
        resp = requests.post(base_url + '/api/datasets/' + str(dataset_dbid) + '/actions/:publish?type=major&key=' + api_token)
        print(resp)
