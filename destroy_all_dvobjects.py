from pyDataverse.api import NativeApi
import json
import dvconfig
import requests
import os
base_url = dvconfig.base_url
api_token = dvconfig.api_token
try:
    api_token=os.environ['API_TOKEN']
    print("Using API token from $API_TOKEN.")
except:
    print("Using API token from config file.")
api = NativeApi(base_url, api_token)

dataverse_ids = []
dataset_ids = []

def main():
    print("Finding dataverses and datasets to destroy...")
    find_children(1)
    dataset_ids.sort(reverse=True)
    for dataset_id in dataset_ids:
        print('Deleting dataset id ' + str(dataset_id))
        print('Preemptively deleting dataset locks for dataset id ' + str(dataset_id))
        resp = requests.delete(base_url + '/api/datasets/' + str(dataset_id) + '/locks?key=' + api_token)
        print(resp)
        resp = requests.delete(base_url + '/api/datasets/' + str(dataset_id) + '/destroy?key=' + api_token)
        print(resp)
    dataverse_ids.sort(reverse=True)
    for dataverse_id in dataverse_ids:
        print('Deleting dataverse id ' + str(dataverse_id))
        resp = api.delete_dataverse(dataverse_id)
        print(resp)
    print("Done.")

def find_children(dataverse_database_id):
    resp = api.get_dataverse_contents(dataverse_database_id, auth=True)
    for dvobject in resp.json()['data']:
        dvtype = dvobject['type']
        dvid = dvobject['id']
        if 'dataverse' == dvtype:
            find_children(dvid)
            dataverse_ids.append(dvid)
        else:
            dataset_ids.append(dvid)

if __name__ == '__main__':
    main()
