import calendar_manager
import datetime

def clear_workout_events():
    service = calendar_manager.get_calendar_service()
    if not service:
        print("Could not authenticate with Google Calendar.")
        return

    # User's calendar ID (default to primary if using service account's own, 
    # or we need the one from user_profile.json if shared)
    # We'll try to load it from user_profile.json
    import json
    try:
        with open('user_profile.json', 'r') as f:
            profile = json.load(f)
            # Fallback to recipient email if calendar_id not explicitly set
            calendar_id = profile.get('calendar_id', profile.get('recipient_email', 'mazzocchilianna@gmail.com'))
    except:
        calendar_id = 'primary'

    print(f"Searching for workout events on calendar: {calendar_id}...")

    # List events
    # We'll look at future events and maybe past ones too? 
    # Let's look from today onwards mostly, or maybe a wide range if they are "practice runs"
    # The screenshot shows many events, likely future recurring or just multiple runs.
    # We'll search for query "Workout:"
    
    page_token = None
    deleted_count = 0
    
    while True:
        events_result = service.events().list(
            calendarId=calendar_id, 
            q="Workout:", # Search query
            singleEvents=True,
            orderBy='startTime',
            pageToken=page_token
        ).execute()
        
        events = events_result.get('items', [])

        for event in events:
            summary = event.get('summary', '')
            if "💪 Workout:" in summary:
                print(f"Deleting event: {summary} ({event['start'].get('dateTime', event['start'].get('date'))})")
                try:
                    service.events().delete(calendarId=calendar_id, eventId=event['id']).execute()
                    deleted_count += 1
                except Exception as e:
                    print(f"Failed to delete event: {e}")

        page_token = events_result.get('nextPageToken')
        if not page_token:
            break

    print(f"Finished. Deleted {deleted_count} events.")

if __name__ == "__main__":
    clear_workout_events()
