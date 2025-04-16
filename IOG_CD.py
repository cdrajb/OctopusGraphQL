#!/usr/bin/env python
# read completed dispatches and write to logfile
import requests,json
from datetime import date, datetime,timezone,timedelta
from requests.models import HTTPError
from zoneinfo import ZoneInfo
import logging

# modify as needed to use the appropriate logging filepath for your OS
# and replace the apikey and accountNumber below with your own

logging.basicConfig(level=logging.INFO,filename="/home/pi/log/IOG_CD.log",filemode="a")
#logging.basicConfig(level=logging.INFO,filename="C:/mydocs~1/personal/House/Octopus/EVSE/log/IOG_CD.log",filemode="a")

url = "https://api.octopus.energy/v1/graphql/"
apikey="sk_live_**********************" # Your Octopus API Key
accountNumber="A-A******" # Your Octopus Account Number

dateTimeToUse = datetime.now().astimezone()
if dateTimeToUse.hour < 17:
    dateTimeToUse = dateTimeToUse-timedelta(days=1)
ioStart = dateTimeToUse.astimezone().replace(hour=23, minute=30, second=0, microsecond=0)
ioEnd = dateTimeToUse.astimezone().replace(microsecond=0).replace(hour=5, minute=30, second=0, microsecond=0)+timedelta(days = 1)

def refreshToken(apiKey,accountNumber):
    try:
        query = """
        mutation krakenTokenAuthentication($api: String!) {
        obtainKrakenToken(input: {APIKey: $api}) {
            token
        }
        }
        """
        variables = {'api': apikey}
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
            query getData($input: String!) {
                completedDispatches(accountNumber: $input) {
                    start
                    end
                    delta
                    meta{source}
                }
            }
        """
        variables = {'input': accountNumber}
        headers={"Authorization": authToken}
        r = requests.post(url, json={'query': query , 'variables': variables, 'operationName': 'getData'},headers=headers)
        return json.loads(r.text)['data']
    except HTTPError as http_err:
        print(f'HTTP Error {http_err}')
    except Exception as err:
        print(f'Another error occurred: {err}')

def getTimes():
    object = getObject()
    return object['completedDispatches']

now = datetime.now()
nowtime=now.strftime('%Y-%m-%d %H:%M:%S')
logging.info('\n')
logging.info('Starting octo_cd_log.py at %s',nowtime)

#timeNow = datetime.now(timezone.utc).astimezone()

#Get Token
authToken = refreshToken(apikey,accountNumber)
times = getTimes()

#Convert to the current timezone
for i,time in enumerate(times):
    slotStart = datetime.strptime(time['start'],'%Y-%m-%dT%H:%M:%S%z').astimezone(ZoneInfo("Europe/London"))
    slotEnd = datetime.strptime(time['end'],'%Y-%m-%dT%H:%M:%S%z').astimezone(ZoneInfo("Europe/London"))
    time['start'] = str(slotStart)
    time['end'] = str(slotEnd)
    times[i] = time


#print("completedDispatches: ", times)

if len(times)>0:
    nextRunStart = datetime.strptime(times[0]['start'],'%Y-%m-%d %H:%M:%S%z').astimezone(ZoneInfo("Europe/London"))
    nextRunEnd = datetime.strptime(times[0]['end'],'%Y-%m-%d %H:%M:%S%z').astimezone(ZoneInfo("Europe/London"))
    outputJson = {'CompletedDispatches': times, 'updatedAt': dateTimeToUse}
    outputJsonString = json.dumps(outputJson, indent=4, default=str)
    #print(outputJsonString)
    logging.info(outputJsonString)
else: 
    logging.info("no dispatches today")

