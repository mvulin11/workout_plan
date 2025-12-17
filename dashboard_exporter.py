"""
Dashboard Data Exporter
Generates a JSON file for the dashboard to consume.
Combines workout data and Garmin recovery metrics.
"""

import os
import json
from datetime import date, datetime
from garmin_manager import get_recovery_data


def get_cycle_phase(last_period_str, cycle_length=28):
    """Calculate current cycle phase."""
    last_period = datetime.strptime(last_period_str, "%Y-%m-%d").date()
    today = date.today()
    days_since = (today - last_period).days
    day_in_cycle = (days_since % cycle_length) + 1
    
    if day_in_cycle <= 5:
        phase = "Menstrual"
        energy = "Variable - listen to your body"
        tip = "Lighter weights OK. Focus on form. Rest if needed."
    elif day_in_cycle <= 14:
        phase = "Follicular"
        energy = "HIGH - rising estrogen = strength gains!"
        tip = "BEST time for heavy lifts & PRs! Push hard."
    elif day_in_cycle <= 17:
        phase = "Ovulation"
        energy = "PEAK energy but injury risk higher"
        tip = "Strong lifts possible. Extra warm-up recommended."
    else:
        phase = "Luteal"
        energy = "Moderate - may feel more fatigued"
        tip = "Maintain volume but listen to body."
    
    return {
        "phase": phase,
        "day": day_in_cycle,
        "energy": energy,
        "training_tip": tip
    }


def export_dashboard_data(workout_plan, user_profile):
    """
    Export combined dashboard data to JSON file.
    
    Args:
        workout_plan: The AI-generated workout plan dict
        user_profile: The user's profile with cycle info
    """
    # Get Garmin recovery data
    print("Fetching Garmin recovery data...")
    recovery_data = get_recovery_data()
    
    # Calculate cycle phase
    cycle_info = user_profile.get('menstrual_cycle', {})
    cycle_phase = get_cycle_phase(
        cycle_info.get('last_period_start', '2025-11-27'),
        cycle_info.get('average_cycle_length', 28)
    )
    
    # Build dashboard data
    dashboard_data = {
        "last_updated": datetime.now().isoformat(),
        "current_week": user_profile.get('current_week', 1),
        "cycle_phase": cycle_phase,
        "recovery": {
            "sleep_score": recovery_data.get("sleep_score"),
            "sleep_hours": recovery_data.get("sleep_duration_hours"),
            "sleep_quality": recovery_data.get("sleep_quality"),
            "body_battery": recovery_data.get("body_battery_current"),
            "hrv_status": recovery_data.get("hrv_status"),
            "recovery_ready": recovery_data.get("recovery_ready", True),
            "notes": recovery_data.get("recovery_notes", [])
        },
        "coaching_notes": workout_plan.get("coaching_notes", ""),
        "workouts": {}
    }
    
    # Add workout days
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for day in days:
        if day in workout_plan:
            dashboard_data["workouts"][day] = workout_plan[day]
    
    # Write to file
    output_path = os.path.join(os.path.dirname(__file__), 'dashboard_data.json')
    with open(output_path, 'w') as f:
        json.dump(dashboard_data, f, indent=2)
    
    print(f"Dashboard data exported to {output_path}")
    return output_path


def export_garmin_only():
    """Export just Garmin data (for daily updates)."""
    # Load existing dashboard data
    data_path = os.path.join(os.path.dirname(__file__), 'dashboard_data.json')
    
    if os.path.exists(data_path):
        with open(data_path, 'r') as f:
            dashboard_data = json.load(f)
    else:
        dashboard_data = {}
    
    # Fetch fresh Garmin data
    print("Fetching Garmin recovery data...")
    recovery_data = get_recovery_data()
    
    # Update just the recovery section
    dashboard_data["recovery"] = {
        "sleep_score": recovery_data.get("sleep_score"),
        "sleep_hours": recovery_data.get("sleep_duration_hours"),
        "sleep_quality": recovery_data.get("sleep_quality"),
        "body_battery": recovery_data.get("body_battery_current"),
        "hrv_status": recovery_data.get("hrv_status"),
        "recovery_ready": recovery_data.get("recovery_ready", True),
        "notes": recovery_data.get("recovery_notes", [])
    }
    dashboard_data["last_updated"] = datetime.now().isoformat()
    
    # Also update cycle phase
    dashboard_data["cycle_phase"] = get_cycle_phase("2025-11-27", 28)
    
    # Write back
    with open(data_path, 'w') as f:
        json.dump(dashboard_data, f, indent=2)
    
    print(f"Garmin data updated in {data_path}")
    return data_path


if __name__ == "__main__":
    # Test: Export Garmin data only
    export_garmin_only()
