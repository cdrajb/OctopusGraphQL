#!/usr/bin/env python
# get Octopus account details
#import sys
#print(sys.path)
import requests,json
from datetime import date, datetime,timezone,timedelta
from requests.models import HTTPError
from include import creds
realm = 'api'
baseurl="https://api.octopus.energy"
url = baseurl + "/v1/accounts/" + creds.accountNumber
api_key = creds.apikey

print("url:",url)

try:
    r = requests.get(url=url, auth=(api_key, ''))
    output_dict = r.json()
    print("Account:", output_dict['number'])
    print("property_id:",output_dict['properties'][0]['id'])
    print("Address:",output_dict['properties'][0]['address_line_1'],output_dict['properties'][0]['town'])
    print("electricity MPAN",output_dict['properties'][0]['electricity_meter_points'][0]['mpan'])
    print("gas MPRN",output_dict['properties'][0]['gas_meter_points'][0]['mprn'])
except HTTPError as http_err:
    print(f'HTTP Error {http_err}')
except Exception as err:
    print(f'Another error occurred: {err}')

