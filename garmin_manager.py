"""
Garmin Connect Manager
Fetches sleep, stress, body battery, and HRV data for recovery-informed training.
"""

import os
import json
from datetime import date, timedelta
from garminconnect import Garmin, GarminConnectAuthenticationError


def get_garmin_client():
    """
    Authenticate with Garmin Connect and return a client.
    Tokens are automatically stored in ~/.garminconnect by the library.
    """
    email = os.environ.get('GARMIN_EMAIL')
    password = os.environ.get('GARMIN_PASSWORD')
    
    if not email or not password:
        print("Warning: GARMIN_EMAIL or GARMIN_PASSWORD not set")
        return None
    
    try:
        # Create client with credentials - library handles token storage automatically
        garmin = Garmin(email=email, password=password)
        garmin.login()
        print(f"Garmin: Logged in as {garmin.display_name}")
        return garmin
        
    except GarminConnectAuthenticationError as e:
        print(f"Garmin authentication error: {e}")
        return None
    except Exception as e:
        print(f"Garmin connection error: {e}")
        return None


def get_recovery_data(target_date=None):
    """
    Fetch comprehensive recovery data from Garmin Connect.
    
    Returns dict with:
    - sleep_score: Overall sleep quality score (0-100)
    - sleep_duration_hours: Hours slept
    - stress_level: Average daily stress (0-100)
    - body_battery: Morning body battery level (0-100)
    - hrv_status: HRV status from Garmin
    - recovery_ready: Boolean indicating if ready for intense training
    """
    # Use yesterday by default - sleep data is more complete
    if target_date is None:
        target_date = date.today() - timedelta(days=1)
    
    # Format date for Garmin API
    date_str = target_date.isoformat()
    
    recovery_data = {
        "date": date_str,
        "sleep_score": None,
        "sleep_duration_hours": None,
        "sleep_quality": None,
        "stress_level": None,
        "body_battery_morning": None,
        "body_battery_current": None,
        "hrv_status": None,
        "recovery_ready": True,
        "recovery_notes": []
    }
    
    client = get_garmin_client()
    if not client:
        recovery_data["recovery_notes"].append("Could not connect to Garmin")
        return recovery_data
    
    try:
        # Fetch Sleep Data
        try:
            sleep_data = client.get_sleep_data(date_str)
            if sleep_data:
                daily_sleep = sleep_data.get('dailySleepDTO', {})
                recovery_data["sleep_score"] = daily_sleep.get('sleepScores', {}).get('overall', {}).get('value')
                
                # Calculate sleep duration in hours
                sleep_seconds = daily_sleep.get('sleepTimeSeconds', 0)
                if sleep_seconds:
                    recovery_data["sleep_duration_hours"] = round(sleep_seconds / 3600, 1)
                
                # Determine sleep quality
                score = recovery_data["sleep_score"]
                if score:
                    if score >= 80:
                        recovery_data["sleep_quality"] = "Excellent"
                    elif score >= 60:
                        recovery_data["sleep_quality"] = "Good"
                    elif score >= 40:
                        recovery_data["sleep_quality"] = "Fair"
                    else:
                        recovery_data["sleep_quality"] = "Poor"
                        recovery_data["recovery_notes"].append("Poor sleep - consider lighter workout")
        except Exception as e:
            print(f"Error fetching sleep data: {e}")
        
        # Fetch Stress Data
        try:
            stress_data = client.get_stress_data(date_str)
            if stress_data:
                avg_stress = stress_data.get('overallStressLevel')
                if avg_stress:
                    recovery_data["stress_level"] = avg_stress
                    if avg_stress > 50:
                        recovery_data["recovery_notes"].append(f"High stress ({avg_stress}) - include mindfulness")
        except Exception as e:
            print(f"Error fetching stress data: {e}")
        
        # Fetch Body Battery
        try:
            body_battery = client.get_body_battery(date_str)
            if body_battery and len(body_battery) > 0:
                # Get morning (first reading) and current (last reading)
                readings = body_battery[0].get('bodyBatteryValuesArray', [])
                if readings:
                    # Morning reading (around 6-8 AM)
                    morning_readings = [r for r in readings if r[0] and 6 <= (r[0] // 3600000) % 24 <= 9]
                    if morning_readings:
                        recovery_data["body_battery_morning"] = morning_readings[0][1]
                    
                    # Current/latest reading
                    valid_readings = [r[1] for r in readings if r[1] is not None]
                    if valid_readings:
                        recovery_data["body_battery_current"] = valid_readings[-1]
        except Exception as e:
            print(f"Error fetching body battery: {e}")
        
        # Fetch HRV Status
        try:
            hrv_data = client.get_hrv_data(date_str)
            if hrv_data:
                hrv_summary = hrv_data.get('hrvSummary', {})
                status = hrv_summary.get('status')
                if status:
                    recovery_data["hrv_status"] = status
                    if status in ['LOW', 'POOR']:
                        recovery_data["recovery_notes"].append("Low HRV - prioritize recovery")
        except Exception as e:
            print(f"Error fetching HRV data: {e}")
        
        # Determine overall recovery readiness
        recovery_data["recovery_ready"] = _calculate_recovery_readiness(recovery_data)
        
    except Exception as e:
        print(f"Error fetching Garmin data: {e}")
        recovery_data["recovery_notes"].append(f"Error: {str(e)}")
    
    return recovery_data


def _calculate_recovery_readiness(data):
    """
    Determine if ready for intense training based on recovery metrics.
    Returns True if ready, False if should take it easy.
    """
    red_flags = 0
    
    # Check sleep
    if data.get("sleep_score") and data["sleep_score"] < 50:
        red_flags += 1
    if data.get("sleep_duration_hours") and data["sleep_duration_hours"] < 6:
        red_flags += 1
    
    # Check stress
    if data.get("stress_level") and data["stress_level"] > 60:
        red_flags += 1
    
    # Check body battery
    if data.get("body_battery_morning") and data["body_battery_morning"] < 30:
        red_flags += 1
    
    # Check HRV
    if data.get("hrv_status") in ['LOW', 'POOR']:
        red_flags += 1
    
    # Ready if 0-1 red flags, not ready if 2+
    return red_flags < 2


def get_recovery_context_for_ai():
    """
    Get a formatted string of recovery data for the AI coach.
    """
    data = get_recovery_data()
    
    context_parts = []
    
    if data["sleep_score"]:
        context_parts.append(f"Sleep: {data['sleep_score']}/100 ({data['sleep_quality']})")
    if data["sleep_duration_hours"]:
        context_parts.append(f"Slept: {data['sleep_duration_hours']}hrs")
    if data["stress_level"]:
        context_parts.append(f"Stress: {data['stress_level']}/100")
    if data["body_battery_current"]:
        context_parts.append(f"Body Battery: {data['body_battery_current']}%")
    if data["hrv_status"]:
        context_parts.append(f"HRV: {data['hrv_status']}")
    
    if not data["recovery_ready"]:
        context_parts.append("⚠️ Recovery metrics suggest taking it easier today")
    
    if data["recovery_notes"]:
        context_parts.append("Notes: " + "; ".join(data["recovery_notes"]))
    
    return "\n".join(context_parts) if context_parts else "No Garmin data available"


# For testing
if __name__ == "__main__":
    print("Testing Garmin Connect integration...")
    
    # Set credentials from environment or directly for testing
    if not os.environ.get('GARMIN_EMAIL'):
        os.environ['GARMIN_EMAIL'] = 'mazzocchilianna@gmail.com'
        os.environ['GARMIN_PASSWORD'] = 'D@kota-072202'
    
    data = get_recovery_data()
    print("\nRecovery Data:")
    print(json.dumps(data, indent=2))
    
    print("\nAI Context:")
    print(get_recovery_context_for_ai())
