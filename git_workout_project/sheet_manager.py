import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# Path to the credentials file provided by the user
CREDENTIALS_FILE = 'gen-lang-client-0542545748-1653ac1bd093.json'
SCOPE = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

def get_last_week_logs(sheet_name="My Workout Plan"):
    """
    Connects to Google Sheets using the service account and fetches logs.
    """
    print(f"Connecting to Google Sheets: {sheet_name}...")
    
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
        client = gspread.authorize(creds)
        
        # Open the spreadsheet
        sheet = client.open(sheet_name)
        
        # Assuming the first worksheet contains the logs, or we look for a specific tab
        # For now, let's grab the first worksheet
        worksheet = sheet.sheet1
        
        # Get all values
        all_values = worksheet.get_all_records()
        
        # If empty, return a message
        if not all_values:
            return "No logs found in the sheet."
            
        # Simple logic: Return the last 10-20 rows as 'recent context'
        # In a real app, we'd filter by date (last 7 days)
        recent_logs = all_values[-20:] if len(all_values) > 20 else all_values
        
        return recent_logs

    except gspread.exceptions.SpreadsheetNotFound:
        return f"Error: Spreadsheet '{sheet_name}' not found. Please share it with the service account email."
    except FileNotFoundError:
        return f"Error: Credentials file '{CREDENTIALS_FILE}' not found."
    except Exception as e:
        return f"Error reading sheet: {str(e)}"

def get_historical_data(sheet_name="My Workout Plan"):
    """
    Fetches all historical data to plot progress.
    Returns a list of dictionaries.
    """
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
        client = gspread.authorize(creds)
        sheet = client.open(sheet_name)
        worksheet = sheet.sheet1
        return worksheet.get_all_records()
    except Exception as e:
        print(f"Error fetching historical data: {e}")
        return []

def log_week_to_sheet(sheet_name, weekly_plan_data, week_number, phase, profile):
    """
    Appends the generated weekly plan to the 'WorkoutLog' tab in Google Sheets.
    Now supports AI-driven per-exercise sets/reps (phase can be None).
    """
    print(f"Logging Week {week_number} to Google Sheet...")
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
        client = gspread.authorize(creds)
        sheet = client.open(sheet_name)
        
        # Get or create WorkoutLog tab
        try:
            worksheet = sheet.worksheet("WorkoutLog")
        except gspread.exceptions.WorksheetNotFound:
            worksheet = sheet.add_worksheet(title="WorkoutLog", rows=100, cols=20)
            # Add header if new (Matches improved_apps_script.js)
            worksheet.append_row(["Week", "Day", "Exercise", "Sets", "Reps", "Rest", "Target Weight", "ACTUAL Weight", "ACTUAL Reps", "RPE", "Coach Cues", "My Notes", "Done"])

        # Find the first empty row based on Column A (Week)
        col_a_values = worksheet.col_values(1)
        next_row = len(col_a_values) + 1
        
        # If header is missing (e.g. cleared sheet), add it
        if next_row == 1:
             worksheet.append_row(["Week", "Day", "Exercise", "Sets", "Reps", "Rest", "Target Weight", "ACTUAL Weight", "ACTUAL Reps", "RPE", "Coach Cues", "My Notes", "Done"])
             next_row = 2

        rows_to_add = []
        
        # Add a separator/header row for the week
        phase_name = phase['name'] if phase else "AI Coached"
        rows_to_add.append([f"WEEK {week_number} - {phase_name}", "", "", "", "", "", "", "", "", "", "", "", ""])

        # Sort days to match schedule order
        day_order = [d['day_name'] for d in profile['schedule_slots']]
        
        for day_name in day_order:
            if day_name not in weekly_plan_data:
                continue
            
            exercises = weekly_plan_data[day_name]
            if not isinstance(exercises, list):
                continue
            
            for ex in exercises:
                exercise_name = ex.get('exercise', 'Unknown')
                
                # Use AI-provided values if available, fallback to phase or defaults
                if phase:
                    sets = phase.get('sets', 3)
                    reps = phase.get('reps', '10')
                    rest = phase.get('rest', '60s')
                    # Calculate weight from phase intensity
                    max_weight = profile['maxes'].get(exercise_name)
                    if max_weight:
                        cycle_count = (week_number - 1) // 4
                        adjusted_max = max_weight * (1 + (cycle_count * 0.025))
                        intensity = phase.get('intensity', 0.7)
                        weight = round((adjusted_max * intensity) / 5) * 5
                        weight_str = f"{weight} lbs"
                    else:
                        weight_str = "RPE 7-8"
                else:
                    # AI-driven: use per-exercise values
                    sets = ex.get('sets', 3)
                    reps = ex.get('reps', '10')
                    rest = ex.get('rest', '60s')
                    weight_str = ex.get('target_weight', 'RPE 7-8')

                row = [
                    week_number,
                    day_name,
                    exercise_name,
                    sets,
                    reps,
                    rest,
                    weight_str,
                    "",  # ACTUAL Weight
                    "",  # ACTUAL Reps
                    "",  # RPE
                    ex.get('cues', ''),
                    "",  # My Notes
                    False  # Done (Checkbox unchecked)
                ]
                rows_to_add.append(row)
            
            # Add an empty row between days
            rows_to_add.append(["", "", "", "", "", "", "", "", "", "", "", "", ""])

        # Use update to write to the specific range
        # Calculate end range
        end_row = next_row + len(rows_to_add) - 1
        range_name = f"A{next_row}:M{end_row}"
        worksheet.update(range_name=range_name, values=rows_to_add)
        
        print(f"Successfully logged workout to sheet (Rows {next_row}-{end_row}).")
        return True

    except Exception as e:
        print(f"Error logging to sheet: {e}")
        return False

if __name__ == "__main__":
    # Test run
    logs = get_last_week_logs()
    print(json.dumps(logs, indent=2))
