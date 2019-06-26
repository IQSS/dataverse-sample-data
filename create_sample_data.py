from pyDataverse.api import Api
import json
import dvconfig
base_url = dvconfig.base_url
api_token = dvconfig.api_token
paths = dvconfig.sample_data
api = Api(base_url, api_token)
print(api.status)
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
    else:
        print('Creating ' + dvtype + ' ' + json_file + ' in dataverse ' + parent)
        dataset_json = path
        with open(dataset_json) as f:
            metadata = json.load(f)
        dataverse = parent
        resp = api.create_dataset(dataverse, json.dumps(metadata))
        print(resp)
        # TODO: upload files
        #dataset_pid = resp.json()['data']['persistentId']
        #tabular_file = 'data/dataverses/open-source-at-harvard/datasets/open-source-at-harvard/files/2019-02-25.tsv'
        #resp = api.upload_file(dataset_pid, tabular_file)
        #print(resp)
