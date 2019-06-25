from pyDataverse.api import Api
import json
import dvconfig
base_url = dvconfig.base_url
api_token = dvconfig.api_token
api = Api(base_url, api_token)
username = 'dataverseAdmin'
password = 'admin1'
endpoint = '/builtin-users/' + username + '/api-token'
params = {}
params['password'] = password
resp = api.get_request(endpoint, params=params, auth=True)
api_token = resp.json()['data']['message']
print(api_token)
