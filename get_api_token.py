from pyDataverse.api import Api
import json
import dvconfig
from pathlib import Path
import os
import sys

base_url = dvconfig.base_url
api = Api(base_url, '')

username = os.getenv('DATAVERSE_USER', 'dataverseAdmin')
password = os.getenv('DATAVERSE_PASSWORD', 'admin1')
# On K8s or with Docker we should get secrets from files, not env vars
if Path(password).is_file():
    f = open(Path(password), 'r')
    password = f.read().strip()
    f.close()

endpoint = '/builtin-users/' + username + '/api-token'
params = {}
params['password'] = password

resp = api.get_request(endpoint, params=params, auth=False)
if resp.json()['status'] == "OK":
    api_token = resp.json()['data']['message']
    print(api_token)
    sys.exit(0)
else:
    print("ERROR receiving API token:", file=sys.stderr)
    print(resp.json(), file=sys.stderr)
    print("Did you enable :AllowApiTokenLookupViaApi configuration option?", file=sys.stderr)
    print("See http://guides.dataverse.org/en/latest/installation/config.html#allowapitokenlookupviaapi", file=sys.stderr)
    sys.exit(1)
