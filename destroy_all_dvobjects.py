from pyDataverse.api import Api
import json
import dvconfig
base_url = dvconfig.base_url
api_token = dvconfig.api_token
api = Api(base_url, api_token)
print('API status: ' +api.status)

dataverse_ids = []
dataset_ids = []

def main():
    print("Finding dataverses and datasets to destroy...")
    find_children(1)
    dataset_ids.sort(reverse=True)
    for dataset_id in dataset_ids:
        print('Deleting dataset id ' + str(dataset_id))
        # If you can't delete a dataset due to a lock, try this:
        # curl -H "X-Dataverse-key: $ADMIN_API_TOKEN" -X DELETE "$SERVER_URL/api/datasets/$ID/locks"
        resp = api.delete_dataset(dataset_id, is_pid=False)
        print(resp)
    dataverse_ids.sort(reverse=True)
    for dataverse_id in dataverse_ids:
        print('Deleting dataverse id ' + str(dataverse_id))
        resp = api.delete_dataverse(dataverse_id)
        print(resp)
    print("Done.")

def find_children(dataverse_database_id):
    query_str = '/dataverses/' + str(dataverse_database_id) + '/contents'
    params = {}
    resp = api.get_request(query_str, params=params, auth=True)
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
