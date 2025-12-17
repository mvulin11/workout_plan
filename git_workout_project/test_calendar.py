import calendar_manager
import os

# Test with the user's email as the calendar ID
calendar_id = 'mazzocchilianna@gmail.com'

print(f"Testing Calendar Access for: {calendar_id}")

service = calendar_manager.get_calendar_service()

if service:
    print("Service authenticated successfully.")
    try:
        # Try to create a simple test event
        calendar_manager.create_workout_event(
            service, 
            "Monday", 
            "TEST EVENT: AI Workout Generator Connection Verified", 
            calendar_id
        )
        print("Test event creation attempted.")
    except Exception as e:
        print(f"Failed to create event: {e}")
else:
    print("Failed to authenticate service.")
