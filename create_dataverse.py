from pyDataverse.api import Api
import json
import dvconfig
base_url = dvconfig.base_url
api_token = dvconfig.api_token
api = Api(base_url, api_token)
print(api.status)
dv_json = 'data/dataverses/open-source-at-harvard/open-source-at-harvard.json'
with open(dv_json) as f:
    metadata = json.load(f)
print(metadata)
# FIXME: Why is "identifier" required?
identifier = metadata['alias']
parentdv = ':root'
resp = api.create_dataverse(identifier, json.dumps(metadata), parent=parentdv)
print(resp)
