#import packages
from datetime import datetime
import requests
import pprint
import json
import time

#if there is any new weather alerts in MO, add list of current weather alerts to JSON file saved in working directory
def alerts(area="MO"):
    #api call to get MO weather alert data
    url = f'https://api.weather.gov/alerts/active/area/{area}'
    result = requests.get(url)
    new_data = json.loads(result.content)
    #open file
    with open('MO_alerts_log_v2.json', 'r+') as f:
        log = json.loads(f.read())
    #define date and time strings
    update_date = new_data['updated'][:10]
    update_time = new_data['updated'][11:]
    #check if date already exists in database 
    try:
        log[update_date]
    #create empty dictionary if date does not yet exist
    except:
        log[update_date] = {}
    #generate list of current events as new entry in database
    new_list = [{'event':new_data['features'][i]['properties']['event'],
                'issued':new_data['features'][i]['properties']['effective'],
                'expires':new_data['features'][i]['properties']['expires'],
                'counties affected':new_data['features'][i]['properties']['areaDesc'],
                'description':new_data['features'][i]['properties']['description'].replace('\n', ' '),
                }
                for i in range(len(new_data['features']))
                ]
    #store new alerts list in database
    log[update_date][update_time] = new_list
    #save database as JSON file on computer
    with open('MO_alerts_log_v2.json', 'w') as f:
        f.write(str(json.dumps(log, indent=2)))
    #return
    return(new_data)

#run script every 5 minutes
while True:
    pprint.pprint(alerts())
    print()
    print(f'last run: {datetime.now()}')
    time.sleep(300)