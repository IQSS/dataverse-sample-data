from pyDataverse.api import NativeApi
from pyDataverse.models import Datafile
import json
import dvconfig
import os
import time
import requests
from io import StringIO
base_url = dvconfig.base_url
api_token = dvconfig.api_token
try:
    api_token=os.environ['API_TOKEN']
    print("Using API token from $API_TOKEN.")
except:
    print("Using API token from config file.")
paths = dvconfig.sample_data
api = NativeApi(base_url, api_token)
print(api.get_info_version())
# TODO limit amount of recursion
def check_dataset_lock(dataset_pid):
    resp = api.get_dataset_lock(dataset_pid)
    locks = resp.json()['data']
    if (locks):
        print('Lock found for dataset id ' + str(dataset_pid) + '... sleeping...')
        time.sleep(2)
        check_dataset_lock(dataset_pid)
resp = api.get_dataverse(':root')
buff = StringIO("")
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
        identifier = metadata['alias']
        resp = api.create_dataverse(parent, json.dumps(metadata))
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
        filemetadata_dir = path.replace(json_file, '') + '.filemetadata'
        print(files_dir)
        for path,subdir,files in os.walk(files_dir):
           for name in files:
                filepath = os.path.join(path,name)
                relpath = os.path.relpath(filepath,files_dir)
                # "directoryLabel" is used to populate "File Path"
                directoryLabel, filename = os.path.split(relpath)
                df = Datafile()
                df_filename = filepath
                df.set({"pid": dataset_pid, "filename": df_filename})
                resp = api.upload_datafile(dataset_pid, df_filename, df.json())
                print(resp)
                file_id = resp.json()['data']['files'][0]['dataFile']['id']
                ## This lock check and sleep is here to prevent the dataset from being permanently
                ## locked because a tabular file was uploaded first.
                check_dataset_lock(dataset_pid)
                # TODO: Think more about where the description comes from. A "sidecar" file as proposed at https://github.com/IQSS/dataverse/issues/5924#issuecomment-499605672 ?
                # L.A.: I implemented something along these lines - an (optional) directory called ".filemetadata" 
                # in the dataset directory, where files containing extra json filemetadata records may be 
                # placed for each of the files in the "files" directory. 
                # check for optional filemetadata file:
                filemetadatapath = os.path.join(filemetadata_dir, relpath);
                if (os.path.exists(filemetadatapath)):
                    with open(filemetadatapath) as m:
                        file_metadata = json.load(m)
                else:
                    file_metadata = {}
                file_metadata['directoryLabel'] = directoryLabel
                jsonData = json.dumps(file_metadata)
                data = { 'jsonData' : jsonData }
                headers = {
                    'X-Dataverse-key': api_token,
                }
                resp = requests.post(base_url + '/api/files/' + str(file_id) + '/metadata', data=data, headers=headers, stream=True, files=buff)
                print(resp)
                # and finally, restrict the file if requested (in the same optional file metadata file, above):
                if 'restricted' in file_metadata.keys():
                    if (file_metadata['restricted']):
                        headers['Content-Type'] = 'application/octet-stream'
                        resp = requests.put(base_url + '/api/files/' + str(file_id) + '/restrict', data='true', headers=headers)
                        print(resp)
        # Sleep a little more to avoid org.postgresql.util.PSQLException: ERROR: deadlock detected
        time.sleep(2)
        print('Publishing dataset id ' + str(dataset_dbid))
        # TODO: Switch to pyDataverse api.publish_dataset after this issue is fixed: https://github.com/AUSSDA/pyDataverse/issues/24
        resp = requests.post(base_url + '/api/datasets/' + str(dataset_dbid) + '/actions/:publish?type=major&key=' + api_token)
        print(resp)
