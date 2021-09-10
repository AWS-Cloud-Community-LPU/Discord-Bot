from datetime import datetime
import os.path
from string import Template
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import constants as C


def get_time():
    """Gets Current Time
    Returns:
        HH:MM:SS {AM/PM} DD/MM/YYYY
    """
    return datetime.now().strftime('%I:%M:%S %p %d/%m/%Y')


def print_logs(log_message):
    """Writes logs in logs.txt
    """
    line = "-------------\n"
    log_message = line + log_message + line
    with open(C.LOG_FILE, 'a+', encoding='utf8') as log_file:
        print(log_message, file=log_file)


# Scope of Google Calendar API
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def fetch_events():
    """Fetches Event from google Calender.

    Returns:
    Events: JSON
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w', encoding='utf8') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.now().astimezone().isoformat()

    # Call the Calendar API
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events


def get_events():
    """Fetches events from F.fetch_events()

    Return:
    String: events in a proper format.
    """
    events = fetch_events()
    event_counter = 1
    # If list is empty
    if not events:
        return "No upcoming events found."
    e_message = ""
    for event in events:
        start = event['start']['dateTime']
        start = start[:-6]
        end = event['end']['dateTime']
        end = end[:-6]
        start = datetime.strptime(
            start, '%Y-%m-%dT%H:%M:%S').strftime('%I:%M %p %d/%m/%Y')
        end = datetime.strptime(
            end, '%Y-%m-%dT%H:%M:%S').strftime('%I:%M %p %d/%m/%Y')
        summary = event['summary']
        try:
            description = event['description']
        except KeyError:
            description = "None"
        try:
            meet_link = event['hangoutLink']
        except KeyError:
            meet_link = "None"
        e_message = e_message + Template(C.EVENTS_TEMPLATE).substitute(
            eno=event_counter, start=start, end=end, summary=summary,
            description=description, meet_link=meet_link)
        event_counter = event_counter + 1
        e_message = e_message + "\n"
    return e_message
