### Convert Single Event to Recurring Event

Converts one-time all-day events (like birthdays) to recurring events. Selection of a specific Google calendar, and events between a start-date and end-date is possible.

Uses _google-api-python-client_ with _Authorized API access (OAuth 2.0)_.

Steps:

* Follow [this](https://developers.google.com/google-apps/calendar/quickstart/python) tutorial, to turn on Google Calendar API and to install google-api-python-client package
* Download `client_secret.json` file to the pwd
* Run the script and authorize the OAuth application when prompted.

NOTE: RRULE in the script is `RRULE:FREQ=YEARLY` (Annually occurring) but can be easily [changed](http://www.kanzaki.com/docs/ical/rrule.html) based on the requirement. However, take note that this script was intended for only converting "All-Day" events. Timezone should be taken into consideration when working with time based events.
