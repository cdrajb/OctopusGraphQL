#!/usr/bin/env python
# read usage and rates 
import sys
import requests,json
from datetime import date, datetime,timezone,timedelta
from requests.models import HTTPError
from zoneinfo import ZoneInfo
import logging
from include import creds

# modify as needed to use the appropriate logging filepath for your OS
# and replace the apikey and accountNumber below with your own

#logging.basicConfig(level=logging.INFO,filename="/home/pi/log/IOG_rates.log",filemode="a")
logging.basicConfig(level=logging.INFO,filename="C:/mydocs~1/personal/House/Octopus/utils/GraphQL/IOG_rates.log",filemode="a")

url = "https://api.octopus.energy/v1/graphql/"

timezone="Europe/London"
startAt="2025-05-07T23:00:00Z"
endAt="2025-05-08T23:00:00Z"

utilityFilters= [{
            "electricityFilters": {
                "readingFrequencyType": "THIRTY_MIN_INTERVAL",
                "marketSupplyPointId": "2000050660710",
                "readingDirection": "CONSUMPTION"}}]

def refreshToken(apiKey,accountNumber):
    try:
        query = """
        mutation krakenTokenAuthentication($api: String!) {
        obtainKrakenToken(input: {APIKey: $api}) {
            token
        }
        }
        """
        variables = {'api': creds.apikey}
        r = requests.post(url, json={'query': query , 'variables': variables})
    except HTTPError as http_err:
        print(f'HTTP Error {http_err}')
    except Exception as err:
        print(f'Another error occurred: {err}')

    jsonResponse = json.loads(r.text)
    return jsonResponse['data']['obtainKrakenToken']['token']

def getObject():
    try:
        query = """
        query GetSmartUsage($propertyId: ID!, 
          $timezone: String!, $startAt: DateTime!, $endAt: DateTime!, 
          $utilityFilters: [UtilityFiltersInput!]!) { property(id: $propertyId) 
          { measurements(first: 1000, timezone: $timezone, 
          startAt: $startAt, endAt: $endAt, utilityFilters: $utilityFilters) 
          { edges { node { __typename value unit ... on 
          IntervalMeasurementType { startAt endAt } 
          metaData { utilityFilters { __typename ... on 
          ElectricityFiltersOutput { readingDirection } ... on 
          GasFiltersOutput { __typename } } statistics { label value type 
          costInclTax { costCurrency estimatedAmount } 
          costExclTax { costCurrency estimatedAmount } } } } } } } }            """
        variables = {"propertyId":creds.propertyId, "timezone":timezone, "startAt":startAt, "endAt":endAt, "utilityFilters":utilityFilters}
        headers={"Authorization": authToken} # request headers must be a dict, not a string
        r = requests.post(url, json={"query": query , "variables": variables},headers=headers)
#        print("Response: ", r.status_code)
        if r.status_code == 400:
            print("Error 400: malformed request")
            sys.exit()
        d = json.loads(r.text)
        return d
    except HTTPError as http_err:
        print(f'HTTP Error {http_err}')
    except Exception as err:
        print(f'Another error occurred: {err}')

def getTimes():
   object = getObject()
#   print(object)
   return object['data']['property']['measurements']['edges']

now = datetime.now()
nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
logging.info('\n')
logging.info('Starting IOG_check_rates.py at %s',nowtime)

#Get Token
authToken = refreshToken(creds.apikey,creds.account_num)
times = getTimes()

for item in times:
    print(item['node']['value'],item['node']['startAt'],item['node']['endAt'],item['node']['metaData']['statistics'][1]['label'])


