#!/usr/bin/env python
'''
Slack - Zabbix Integration Webhook
A Slack incoming webhook to show events from Zabbix.

Usage: slack_zabbix.py <to> <subject> <message>

See the README for more information
'''

import json
import httplib2
import sys

# personal webhook url from slack
hookurl = ""

##
########################################################
## only change below here if you know what you are doing
def usage():
    print "slack_zabbix.py <to> <subject> <message>\n\
    \n\
    <to>        channel or person\n\
    <subject>   subject line\n\
    <message>   message body\n\
    \n\
    example: slack_zabbix.py '#alerts' 'PROBLEM' 'Average :: Zabbix server :: Zabbix discoverer processes more than 75% busy :: http://host.domain.tld/tr_events.php?triggerid={TRIGGER.ID}&eventid={EVENT.ID} :: http://host.domain.tld/acknow.php?eventid={EVENT.ID}&triggerid={TRIGGER.ID}&backurl=dashboard.php'"

def main():
    try:
        args = sys.argv[1:]
    except:
        usage()
        sys.exit(2)
    
    # parse command line input
    channel = args[0]
    status = args[1]
    result = args[2].split(' :: ')
    severity = result[0]
    device = result[1]
    message = result[2]
    detail_url = result[3]
    ack_url = result[4]
    summary = device + ": " + status + ": " + message

    # set the color based on severity
    if status == "OK":
        color = "good" #green
    elif severity == "Disaster":
        color = "#FF3838"
    elif severity == "High":
        color = "#FF9999"
    elif severity == "Average":
        color = "#FFB689"
    elif severity == "Warning":
        color = "#FFF6A5"
    elif severity == "Information":
        color = "#D6F6FF"
    elif severity == "Not classified":
        color = "#DBDBDB"
    else:
        color = ""
    
    if status == "PROBLEM":
        fields = [{
            "title": "Actions",
            "value": "<" + ack_url + "|Acknowledge>",
            "short": True
        }]
    else:
        fields = [{}]

    attachment = [{
        "fallback": summary,
        "text": message,
        "title": status + ": " + device,
        "title_link": detail_url,
        "color": color,
        "fields": fields
    }]

    # post to slack
    payload = json.dumps({
        "attachments": attachment
    })
    
    h = httplib2.Http()
    (resp, content) = h.request(hookurl, "POST", body=payload, headers={'content-type':'application/json'})
    
if __name__ == "__main__":
    main()