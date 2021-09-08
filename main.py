from datetime import datetime
import os.path
import configparser
from string import Template
import discord
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import constants as C

# Scope of Google Calendar API
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


# Discord authentication
client = discord.Client()
config = configparser.ConfigParser()
config.read('secrets.ini')


@client.event
async def on_message(message):
    """
    Function Invoked when a message is sent on Discord Server.
    """
    if message.author == client.user:
        return

    if message.content.startswith('$events'):
        events = get_events()
        event_counter = 1
        # If list is empty
        if not events:
            await message.channel.send("No upcoming events found.")
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
            e_message = Template(C.EVENTS_TEMPLATE).substitute(
                eno=event_counter, start=start, end=end, summary=summary, description=description, meet_link=meet_link)
            event_counter = event_counter + 1
            await message.channel.send(e_message)


def get_events():
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
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.now().astimezone().isoformat()

    # Call the Calendar API
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events


client.run(config['KEYS']['API_KEY'])
