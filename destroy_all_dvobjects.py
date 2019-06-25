from pyDataverse.api import Api
import json
import dvconfig
base_url = dvconfig.base_url
api_token = dvconfig.api_token
api = Api(base_url, api_token)
print(api.status)
#FIXME: remove hard coded dataverse alias
alias = 'open-source-at-harvard'
query_str = '/dataverses/' + alias + '/contents'
params = {}
params['foo'] = 'bar'
resp = api.get_request(query_str, params=params, auth=True)
print(json.dumps(resp.json(), indent=2))
# FIXME: iterate through all content instead of just looking at index 0.
protocol = resp.json()['data'][0]['protocol']
authority = resp.json()['data'][0]['authority']
identifier = resp.json()['data'][0]['identifier']
dataset_pid = protocol + ':' + authority + '/' + identifier
print(dataset_pid)
resp = api.delete_dataset(dataset_pid)
print(resp)
resp = api.delete_dataverse(alias)
print(resp)
