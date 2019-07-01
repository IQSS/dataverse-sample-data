from pyDataverse.api import Api
import json
import dvconfig
from urllib.parse import urlparse,parse_qs
base_url = dvconfig.base_url
api_token = dvconfig.api_token
api = Api(base_url, api_token)
print('API status: ' +api.status)

def main():
    #dsurl = 'https://demo.dataverse.org/dataset.xhtml?persistentId=doi:10.5072/FK2/U6AEZM'
    dsurl = 'https://demo.dataverse.org/dataset.xhtml?persistentId=doi:10.5072/FK2/PPPORT'
    print(dsurl)
    o = urlparse(dsurl)
    hostname = o.netloc
    doi = parse_qs(o.query)['persistentId'][0]
    curl_native_json = "curl '" + 'https://' + hostname + '/api/datasets/export?exporter=dataverse_json&persistentId=' + doi + "' | jq ."
    print(curl_native_json)

def find_children(dataverse_database_id):
    pass

if __name__ == '__main__':
    main()
