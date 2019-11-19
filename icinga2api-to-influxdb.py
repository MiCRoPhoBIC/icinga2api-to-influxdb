#!/usr/bin/env python3
#Check status for all services from Icinga2 API and write it to InfluxDB
#https://github.com/MiCRoPhoBIC/icinga2api-to-influxdb

import requests, json
from influxdb import InfluxDBClient

#InfluxDB details
client = InfluxDBClient(host='127.0.0.1', port=8086, username='icinga2', password='xxxxx', database='icinga2')
#Icinga2 API URL
request_url = "https://127.0.0.1:5665/v1/objects/services"
headers = {
        'Accept': 'application/json',
        'X-HTTP-Method-Override': 'GET'
        }
data = {
#Attributes to fetch
        "attrs": [ "host_name", "display_name", "state", "downtime_depth", "acknowledgement" ]
#If you decide to filter
#,
#        "filter": "service.state != ServiceOK && service.downtime_depth == 0.0 && service.acknowledgement == 0.0"
}

r = requests.post(request_url,
        headers=headers,
#Username/password for Icinga2 API
        auth=('telegrafapiuser', 'xxxxxxx'),
        data=json.dumps(data),
        verify=False)
#When in production you should enable proper verification
#        verify="/etc/icinga2/pki/ca.crt")


#print(("Request URL: " + str(r.url)))
#print(("Status code: " + str(r.status_code)))

if (r.status_code == 200):
         j = json.loads(r.text)
         for i in j['results']:
          metrics = {}
#Write measurements to icinga2grafanastatus in InfluxDB
          metrics['measurement'] = "icinga2grafanastatus"
          tags = {}
          fields = {}
          metrics['tags'] = tags
          fields['displayname'] = i['attrs']['display_name']
          fields['acknowledgement'] = i['attrs']['acknowledgement']
          fields['downtime_depth'] = i['attrs']['downtime_depth']
          fields['hostname'] = i['attrs']['host_name']
          fields['state'] = i['attrs']['state']
          metrics["fields"] = fields
          metrics=[metrics, ]
          client.write_points(metrics)
#          result = client.query('select state from "icinga2grafanastatus";')
#          print("Result: {0}".format(result))
#          print((metrics))
#         print(json.dumps(j, indent = 4))

else:
        print((r.text))
        r.raise_for_status()
