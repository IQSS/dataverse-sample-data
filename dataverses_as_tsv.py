from pyDataverse.api import Api
import json
import dvconfig
import requests
import csv
base_url = dvconfig.base_url
api_token = dvconfig.api_token
api = Api(base_url, api_token)

root_dataverse_database_id = 1
dataverse_ids = []
tsv_file = 'dataverses.tsv'

def main():
    find_children(root_dataverse_database_id)
    print('Dataverses found (excluding dataverse id ' + str(root_dataverse_database_id) + '): ' + str(len(dataverse_ids)))
    dataverse_ids.sort
    myarray = []
    for dataverse_id in dataverse_ids:
        resp = api.get_dataverse(dataverse_id, auth=True)
        dataverse = resp.json()['data']
        mydict = {}
        dvid = dataverse['id']
        alias = dataverse['alias']
        name = dataverse['name']
        print('Getting info for dataverse: ' + name) 
        affiliation = dataverse['affiliation']
        contact1 = dataverse['dataverseContacts'][0]
        category = dataverse['dataverseType']
        creationdate = dataverse['creationDate']
        ownerid = dataverse['ownerId']
        mydict['id'] = dvid
        mydict['alias'] = alias
        mydict['name'] = name
        mydict['affiliation'] = affiliation
        mydict['contact1'] = contact1['contactEmail']
        mydict['category'] = category
        mydict['creationdate'] = creationdate
        mydict['url'] = base_url + "/dataverse/" + alias
        mydict['parenturl'] = base_url + "/dataverse.xhtml?id=" + str(ownerid)
        myarray.append(mydict)

    keys = myarray[0].keys()
    with open(tsv_file, 'w') as out_file:
        writer = csv.DictWriter(out_file, keys, delimiter='\t')
        writer.writeheader()
        writer.writerows(myarray)

    print("Done. Saved to " + tsv_file)

def find_children(dataverse_database_id):
    query_str = '/dataverses/' + str(dataverse_database_id) + '/contents'
    params = {}
    resp = api.get_request(query_str, params=params, auth=True)
    for dvobject in resp.json()['data']:
        dvtype = dvobject['type']
        dvid = dvobject['id']
        if 'dataverse' == dvtype:
            title = dvobject['title']
            print('Found dataverse id ' + str(dvid) + ': ' + title)
            find_children(dvid)
            dataverse_ids.append(dvid)

if __name__ == '__main__':
    main()
