from __future__ import print_function
import os
from datetime import datetime

import httplib2
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar: Single Event to Recurring Event'


def get_credentials():
    credential_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),
            'credentials.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    page_token = None
    idx = 0
    l = []
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print(str(idx) + ': '+ calendar_list_entry['summary'])
            idx = idx + 1
            l.append(calendar_list_entry['id'])
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    choice = str(raw_input('Select a calendar: '))
    choice = int(choice)
    
    print('\nUse format DD.MM.YYYY')
    start_raw = str(raw_input('Start Date:\t'))
    end_raw = str(raw_input('End Date:\t'))
    try:
        start_date = datetime.strptime(start_raw,'%d.%m.%Y')
        end_date = datetime.strptime(end_raw,'%d.%m.%Y')
    except ValueError:
        print('One of the date is in incorrect format')

    # The API needs a timestamp in RFC3339. Using hardcoded UTC TZ because the events this script was created for are full day events
    start_date = start_date.isoformat('T')+'-00:00'
    end_date = end_date.isoformat('T')+'-00:00'


    '''
        This can be improved using batch processing to reduce HTTP overhead : 
        https://developers.google.com/api-client-library/python/guide/batch
    '''
    page_token = None
    idx = 0
    while True:
      events = service.events().list(calendarId=l[choice], pageToken=page_token, timeMin=start_date, timeMax=end_date).execute()
      for event in events['items']:
        e = service.events().get(calendarId=l[choice], eventId=event['id']).execute()
        '''
            RRULES. RFC-5545
            https://tools.ietf.org/html/rfc5545
            https://nylas.com/blog/rrules/
            http://www.kanzaki.com/docs/ical/rrule.html
        '''
        e['recurrence'] = ['RRULE:FREQ=YEARLY']
        ue = service.events().update(calendarId=l[choice], eventId=event['id'], body=e).execute()
        idx = idx + 1
      page_token = events.get('nextPageToken')
      if not page_token:
	break

    print('\nConverted #%d. Done.'%idx)

if __name__ == '__main__':
    main()

