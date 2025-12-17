from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import json

# Path to the credentials file
CREDENTIALS_FILE = 'credentials.json' # This will be created by the GitHub Action
# For local testing, we might need to point to the specific file or ensure credentials.json exists
# In the GitHub Action, we write the secret to 'credentials.json'.
# Locally, the user has 'gen-lang-client...json'.
# I'll make it robust to check for both or use an env var.

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Authenticates and returns the Calendar service."""
    creds = None
    # Try local specific file first, then generic 'credentials.json'
    local_creds = 'gen-lang-client-0542545748-1653ac1bd093.json'
    
    try:
        if os.path.exists(local_creds):
            creds = service_account.Credentials.from_service_account_file(
                local_creds, scopes=SCOPES)
        elif os.path.exists('credentials.json'):
             creds = service_account.Credentials.from_service_account_file(
                'credentials.json', scopes=SCOPES)
        else:
            print("Error: No credentials file found.")
            return None

        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        print(f"Auth Error: {e}")
        return None

def create_workout_event(service, day_name, exercise_summary, calendar_id='primary'):
    """
    Creates a workout event on the user's calendar.
    
    Args:
        service: The authenticated Calendar service.
        day_name: "Monday", "Tuesday", etc.
        exercise_summary: String description of the workout (e.g., "Leg Day: Squats, Lunges...")
        calendar_id: The ID of the calendar to add to. Defaults to 'primary' (but for Service Accounts, 
                     'primary' is the service account's calendar, NOT the user's. 
                     The user MUST share their calendar and we need that Calendar ID).
    """
    # Calculate the date for the next occurrence of this day
    today = datetime.date.today()
    days_ahead = 0
    
    # Map day names to integers (Monday=0, Sunday=6)
    day_map = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, 
        "Friday": 4, "Saturday": 5, "Sunday": 6
    }
    
    target_day_idx = day_map.get(day_name)
    if target_day_idx is None:
        return
        
    current_day_idx = today.weekday()
    
    # Calculate days until the target day
    days_ahead = target_day_idx - current_day_idx
    if days_ahead <= 0: # If today is Monday and we want Monday, assume next week? Or today?
        # Let's assume we are generating for the UPCOMING week.
        # If running on Sunday (6), Monday (0) is +1 day.
        days_ahead += 7
        
    target_date = today + datetime.timedelta(days=days_ahead)
    
    start_time = f"{target_date}T04:30:00" # 4:30 AM
    end_time = f"{target_date}T05:30:00"   # 5:30 AM
    
    event = {
        'summary': f'💪 Workout: {day_name}',
        'description': exercise_summary,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/New_York', # Hardcoded for now, can be parameterized
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/New_York',
        },
    }

    try:
        event = service.events().insert(calendarId=calendar_id, body=event).execute()
        print(f"Event created: {event.get('htmlLink')}")
    except Exception as e:
        print(f"Error creating event: {e}")

import os
