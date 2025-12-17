import json
import smtplib
import os
import datetime
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import google.generativeai as genai

import sheet_manager
import visualizer
import calendar_manager
import dashboard_exporter

# --- MENSTRUAL CYCLE TRACKING ---
def get_cycle_phase(profile):
    """
    Calculates the current menstrual cycle phase based on last period start date.
    Returns phase info with training recommendations.
    """
    cycle_data = profile.get('menstrual_cycle', {})
    if not cycle_data.get('track_cycle', False):
        return None
    
    last_period = cycle_data.get('last_period_start')
    if not last_period:
        return None
    
    try:
        last_period_date = datetime.datetime.strptime(last_period, '%Y-%m-%d').date()
    except ValueError:
        return None
    
    today = datetime.date.today()
    cycle_length = cycle_data.get('average_cycle_length', 28)
    day_in_cycle = (today - last_period_date).days % cycle_length + 1
    
    # Define phases with training implications
    if 1 <= day_in_cycle <= 5:
        return {
            "phase": "Menstrual",
            "day": day_in_cycle,
            "energy": "Variable - may be lower",
            "training_tip": "Listen to your body. Okay to reduce intensity if needed. Focus on form over load.",
            "intensity_modifier": 0.85  # Slightly reduce if needed
        }
    elif 6 <= day_in_cycle <= 14:
        return {
            "phase": "Follicular",
            "day": day_in_cycle,
            "energy": "HIGH - rising estrogen = strength gains!",
            "training_tip": "BEST time for heavy lifts & PRs! Push hard, increase weights, train intensely.",
            "intensity_modifier": 1.1  # Can push harder
        }
    elif 15 <= day_in_cycle <= 17:
        return {
            "phase": "Ovulation",
            "day": day_in_cycle,
            "energy": "PEAK energy but ligament laxity increases",
            "training_tip": "High energy but be mindful of form. Good for power & HIIT. Warm up well.",
            "intensity_modifier": 1.05
        }
    else:  # 18-28 Luteal
        return {
            "phase": "Luteal",
            "day": day_in_cycle,
            "energy": "Moderate to low - progesterone rising",
            "training_tip": "Maintain volume but may need longer rest. Great for hypertrophy work. Stay hydrated.",
            "intensity_modifier": 0.95
        }

# --- LEGACY PERIODIZATION (kept for reference, AI now decides dynamically) ---
PERIODIZATION_REFERENCE = {
    "Accumulation": {"sets": "3-4", "reps": "10-12", "intensity": "moderate", "rest": "60-90s"},
    "Intensification": {"sets": "3-4", "reps": "6-8", "intensity": "high", "rest": "2-3 mins"},
    "Realization": {"sets": "3-5", "reps": "3-5", "intensity": "very high", "rest": "3-5 mins"},
    "Deload": {"sets": "2-3", "reps": "8-10", "intensity": "low", "rest": "60s"}
}

def load_profile():
    """Loads the user's current stats and progress."""
    try:
        with open('user_profile.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: user_profile.json not found.")
        return None

def save_profile(profile):
    """Saves the updated profile to JSON."""
    with open('user_profile.json', 'w') as f:
        json.dump(profile, f, indent=4)

def calculate_weight(one_rep_max, intensity):
    """Calculates working weight rounded to nearest 5lbs."""
    weight = one_rep_max * intensity
    return round(weight / 5) * 5

def select_exercises_for_week(profile):
    """
    Uses Gemini 3 Pro as the ultimate AI coach.
    The AI decides EVERYTHING: exercises, sets, reps, intensity based on full context.
    Returns a structured dictionary of the week's workout.
    """
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY not set.")
        return None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-3-pro-preview')  # Upgraded to Gemini 3 Pro

    # Get Performance Context from Sheets
    last_week_logs = sheet_manager.get_last_week_logs(profile.get('google_sheet_name', 'My Workout Plan'))
    performance_context = json.dumps(last_week_logs, indent=2)

    # Get Menstrual Cycle Context
    cycle_phase = get_cycle_phase(profile)
    cycle_context = ""
    if cycle_phase:
        cycle_context = f"""
    🔴 MENSTRUAL CYCLE CONTEXT (CRITICAL - adjust training accordingly!):
    - Current Phase: {cycle_phase['phase']} (Day {cycle_phase['day']})
    - Energy Level: {cycle_phase['energy']}
    - Training Recommendation: {cycle_phase['training_tip']}
    """

    # Get Nutrition Context
    nutrition = profile.get('nutrition', {})
    nutrition_context = ""
    if nutrition:
        nutrition_context = f"""
    Nutrition Targets: {nutrition.get('calorie_target', 'N/A')} cal, 
    Protein: {nutrition.get('protein_target_g', 'N/A')}g, 
    Carbs: {nutrition.get('carb_target_g', 'N/A')}g, 
    Fat: {nutrition.get('fat_target_g', 'N/A')}g
    """

    # Prepare context for the AI
    schedule_slots = profile['schedule_slots']
    exercise_db_summary = json.dumps(profile['exercise_database'], indent=2)
    user_context = profile.get('user_context', {})
    maxes = profile.get('maxes', {})
    
    prompt = f"""
    You are Lianna's PERSONAL strength and conditioning coach. You are the ULTIMATE authority on her training.
    Your job is to create the PERFECT workout plan for Week {profile['current_week']}.
    
    🚨 CRITICAL: You have COMPLETE, UNRESTRICTED AUTONOMY:
    - You are NOT limited to the exercise database - CREATE NEW exercises as needed!
    - Design the ENTIRE workout structure from scratch based on her goals
    - Pick ANY exercises that will best achieve her goals (glutes, back, triceps, obliques, quads, calves)
    - Decide sets, reps, rest, and intensity for EACH exercise individually
    - When adding new exercises, ALWAYS provide a valid YouTube URL
    - The exercise database is just a REFERENCE - feel free to go beyond it!
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    👤 LIANNA'S PROFILE
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    - Stats: {user_context.get('stats', 'N/A')}
    - Experience: {user_context.get('experience', 'N/A')}
    - Gym: {user_context.get('gym_profile', 'N/A')}
    - Goals: {user_context.get('specific_goals', profile['primary_goal'])}
    - Known Maxes: {json.dumps(maxes, indent=2)}
    {nutrition_context}
    {cycle_context}
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📊 LAST WEEK'S PERFORMANCE (Analyze this carefully!)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {performance_context}
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📅 TRAINING SCHEDULE
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Training Days: Monday, Tuesday, Wednesday, Thursday, Friday
    
    Day Focus Guidelines (USE AS INSPIRATION, NOT STRICT RULES):
    - Monday: Glutes & Hamstrings focus
    - Tuesday: Upper Body (Back, Shoulders, Arms)
    - Wednesday: Quads, Calves, Core
    - Thursday: Push/Pull/Arms emphasis
    - Friday: Glute Volume & Full Body Accessories
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📚 EXERCISE DATABASE (Reference - you can also suggest new exercises)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {exercise_db_summary}
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    🎯 YOUR COACHING DIRECTIVES (CRITICAL - READ CAREFULLY!)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    ⚠️ WORKOUT VOLUME REQUIREMENTS:
    - MINIMUM 5-6 exercises per day (she wants challenging, complete workouts!)
    - Include 1-2 compound movements per session
    - Include 2-3 isolation/accessory exercises
    - Add 1-2 supersets when appropriate for efficiency
    - Total workout time should be ~60-75 minutes
    
    🏋️ PROGRAMMING PRINCIPLES:
    1. ANALYZE performance data. Adjust based on RPE, notes, and completion.
    2. RESPECT the menstrual cycle phase. Adjust intensity accordingly.
    3. CHALLENGE her! She's intermediate/advanced and wants to be pushed!
    4. VARY exercises week to week. Keep it fresh and hit muscles from different angles.
    5. PROGRESSIVE OVERLOAD. Increase weights, reps, or sets over time.
    6. CUSTOMIZE sets/reps/rest for EACH exercise based on its purpose.
    7. MIX rep ranges: Heavy (5-8), Moderate (8-12), High (12-20) as appropriate.
    8. Include FINISHERS when appropriate (burnout sets, drop sets, etc.)
    
    📹 EXERCISE DETAILS:
    - For new exercises, provide a valid YouTube URL.
    - Provide a short, punchy technical cue for each exercise.
    
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📤 OUTPUT FORMAT (Return ONLY valid JSON, no markdown)
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    {{
        "coaching_notes": "Brief note on this week's focus and why (2-3 sentences)",
        "Monday": [
            {{
                "category": "Category Name",
                "exercise": "Exercise Name",
                "sets": 3,
                "reps": "8-10",
                "rest": "90s",
                "target_weight": "Weight in lbs or 'RPE 7-8'",
                "url": "YouTube URL",
                "cues": "Technical Cue (max 15 words)",
                "is_new": false
            }},
            ... (5-6 exercises minimum per day!)
        ],
        "Tuesday": [...],
        "Wednesday": [...],
        "Thursday": [...],
        "Friday": [...]
    }}
    """

    try:
        response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
        weekly_plan_data = json.loads(response.text)
        
        # Handle potential AI formatting error (List instead of Dict)
        # Handle potential AI formatting error (List instead of Dict)
        if isinstance(weekly_plan_data, list):
            print("Warning: AI returned a list. Attempting to merge into dictionary.")
            merged_data = {}
            for item in weekly_plan_data:
                if isinstance(item, dict):
                    # Check if the dict keys are day names (e.g. {"Monday": [...]})
                    day_keys = [k for k in item.keys() if k in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]]
                    if day_keys:
                        for k in day_keys:
                            merged_data[k] = item[k]
                    
                    # Check if it uses "day" or "day_name" key (e.g. {"day": "Monday", "exercises": [...]})
                    elif "day" in item and "exercises" in item:
                        merged_data[item["day"]] = item["exercises"]
                    elif "day_name" in item and "exercises" in item:
                        merged_data[item["day_name"]] = item["exercises"]
                        
            weekly_plan_data = merged_data

        # Sanitize Data (Ensure all exercises are dicts)
        weekly_plan_data = sanitize_plan_data(weekly_plan_data)

        return weekly_plan_data
    except Exception as e:
        print(f"Gemini API Error during planning: {e}")
        return None

def sanitize_plan_data(data):
    """Ensures the plan data structure is valid (Dict of Lists of Dicts)."""
    if not isinstance(data, dict):
        return {}
    
    sanitized = {}
    for day, exercises in data.items():
        if not isinstance(exercises, list):
            # If it's just a single item (dict or str), wrap in list
            exercises = [exercises]
        
        clean_exercises = []
        for ex in exercises:
            if isinstance(ex, str):
                # Convert string to default dict object
                clean_exercises.append({
                    "exercise": ex,
                    "category": "Unspecified",
                    "sets": "3",
                    "reps": "10",
                    "rest": "60s",
                    "cues": "Focus on form.",
                    "url": f"https://www.youtube.com/results?search_query={ex.replace(' ', '+')}",
                    "is_new": False
                })
            elif isinstance(ex, dict):
                # Ensure 'exercise' key exists
                if 'exercise' not in ex:
                    ex['exercise'] = "Unknown Exercise"
                clean_exercises.append(ex)
        
        sanitized[day] = clean_exercises
    return sanitized

def update_database_with_new_exercises(profile, weekly_plan_data):
    """Checks for new exercises in the AI plan and adds them to the user profile."""
    updates_made = False
    
    for day_name, exercises in weekly_plan_data.items():
        for ex in exercises:
            if ex.get('is_new'):
                category = ex['category']
                # Ensure category exists in DB
                if category not in profile['exercise_database']:
                    profile['exercise_database'][category] = []
                
                # Check if it's really new (avoid duplicates)
                existing_names = [e['name'] for e in profile['exercise_database'][category]]
                if ex['exercise'] not in existing_names:
                    new_entry = {
                        "name": ex['exercise'],
                        "url": ex['url'],
                        "desc": "AI Suggested Variation",
                        "alt": "Standard Variation"
                    }
                    profile['exercise_database'][category].append(new_entry)
                    print(f"Added new exercise to DB: {ex['exercise']} ({category})")
                    updates_made = True
    
    if updates_made:
        save_profile(profile)

import visualizer

# ... (imports)

def generate_html_email(profile, weekly_plan_data):
    """Generates the HTML email content with hyperlinks. Now uses AI-provided sets/reps/weight."""
    
    # Generate Progress Chart
    try:
        historical_data = sheet_manager.get_historical_data(profile.get('google_sheet_name', 'My Workout Plan'))
        chart_base64 = visualizer.generate_progress_chart(historical_data)
        chart_html = f'<img src="data:image/png;base64,{chart_base64}" alt="Progress Chart" style="width:100%; max-width:600px;"/>' if chart_base64 else ""
    except Exception as e:
        print(f"Error generating chart: {e}")
        chart_html = ""

    # Get cycle phase for display
    cycle_phase = get_cycle_phase(profile)
    cycle_html = ""
    if cycle_phase:
        phase_colors = {
            "Menstrual": "#e57373",
            "Follicular": "#81c784", 
            "Ovulation": "#ffb74d",
            "Luteal": "#9575cd"
        }
        phase_color = phase_colors.get(cycle_phase['phase'], "#888")
        cycle_html = f"""
        <div style="background: linear-gradient(135deg, {phase_color}22, {phase_color}44); border-left: 4px solid {phase_color}; padding: 15px; margin: 15px 0; border-radius: 8px;">
            <strong>🔴 Cycle Phase:</strong> {cycle_phase['phase']} (Day {cycle_phase['day']})<br>
            <strong>Energy:</strong> {cycle_phase['energy']}<br>
            <em>{cycle_phase['training_tip']}</em>
        </div>
        """

    # Get coaching notes from AI
    coaching_notes = weekly_plan_data.get('coaching_notes', 'Train hard, stay focused!')

    plan_html = f"""
    <html>
    <body style="font-family: 'Segoe UI', sans-serif; color: #333; background: #f9f9f9; padding: 20px;">
        <div style="max-width: 700px; margin: 0 auto; background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); padding: 30px;">
            <h2 style="color: #d81b60;">💪 {profile.get('user_name', 'Your')} Training Protocol: Week {profile['current_week']}</h2>
            
            {cycle_html}
            
            <div style="background: #f0f7ff; padding: 15px; border-radius: 8px; margin: 15px 0;">
                <strong>🎯 Coach's Notes:</strong><br>
                {coaching_notes}
            </div>
            
            <p><strong>Goal:</strong> {profile['primary_goal']}</p>
            <hr style="border: none; border-top: 2px solid #eee;">
            {chart_html}
            <br>
    """

    # Sort days to match the schedule order in profile
    day_order = [d['day_name'] for d in profile['schedule_slots']]
    
    for day_name in day_order:
        if day_name not in weekly_plan_data:
            continue
            
        exercises = weekly_plan_data[day_name]
        if not isinstance(exercises, list):
            continue
            
        day_focus = next((d['focus'] for d in profile['schedule_slots'] if d['day_name'] == day_name), "Workout")
        
        plan_html += f"<h3 style='color: #d81b60; margin-top: 25px;'>{day_name} - {day_focus}</h3>"
        plan_html += "<table border='0' cellpadding='10' style='border-collapse: collapse; width: 100%; background: #fafafa; border-radius: 8px;'>"
        plan_html += "<tr style='background-color: #d81b60; color: white;'><th>Exercise</th><th>Sets</th><th>Reps</th><th>Weight</th><th>Rest</th><th>Cues</th></tr>"
        
        for i, ex in enumerate(exercises):
            exercise_name = ex.get('exercise', 'Unknown')
            url = ex.get('url', '#')
            cues = ex.get('cues', '')
            sets = ex.get('sets', 3)
            reps = ex.get('reps', '10')
            rest = ex.get('rest', '60s')
            target_weight = ex.get('target_weight', 'RPE 7-8')
            
            row_bg = '#ffffff' if i % 2 == 0 else '#f5f5f5'
            
            plan_html += f"""
            <tr style="background-color: {row_bg};">
                <td><a href="{url}" style="color: #0066cc; text-decoration: none; font-weight: bold;">{exercise_name}</a></td>
                <td style="text-align: center;">{sets}</td>
                <td style="text-align: center;">{reps}</td>
                <td style="text-align: center; font-weight: bold;">{target_weight}</td>
                <td style="text-align: center;">{rest}</td>
                <td><small style="color: #666;">{cues}</small></td>
            </tr>
            """
        plan_html += "</table>"

    plan_html += """
            <br><hr style="border: none; border-top: 2px solid #eee;">
            <p style="color: #888; font-size: 12px;"><em>🤖 Powered by Gemini 3 Pro • Your Personal AI Coach</em></p>
        </div>
    </body>
    </html>
    """
    return plan_html

def send_email(content, recipient_email, week_number):
    """Sends the plan via email."""
    sender_email = os.environ.get('EMAIL_USER')
    sender_password = os.environ.get('EMAIL_PASS')
    
    if not sender_email or not sender_password:
        print("Skipping email: Credentials not set. Saving to 'weekly_plan.html'.")
        with open('weekly_plan.html', 'w') as f:
            f.write(content)
        return

    msg = MIMEMultipart()
    msg['Subject'] = f"Your Training Plan - Week {week_number}"
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg.attach(MIMEText(content, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def update_week(profile):
    """Increments the week number in the JSON file."""
    profile['current_week'] += 1
    save_profile(profile)

if __name__ == "__main__":
    user_profile = load_profile()
    if user_profile:
        print(f"Generating plan for Week {user_profile['current_week']}...")
        
        # Display cycle phase info
        cycle_phase = get_cycle_phase(user_profile)
        if cycle_phase:
            print(f"🔴 Cycle Phase: {cycle_phase['phase']} (Day {cycle_phase['day']})")
            print(f"   Training Tip: {cycle_phase['training_tip']}")
        
        # 1. Select Exercises (AI decides everything!)
        print("Consulting Gemini 3 Pro AI Coach...")
        weekly_workout_data = select_exercises_for_week(user_profile)
        
        if weekly_workout_data:
            # 2. Update DB if new exercises found
            update_database_with_new_exercises(user_profile, weekly_workout_data)
            
            # 3. Generate HTML
            email_html = generate_html_email(user_profile, weekly_workout_data)
            
            # 4. Send Email
            recipient = os.environ.get('RECIPIENT_EMAIL', 'mazzocchilianna@gmail.com')
            send_email(email_html, recipient, user_profile['current_week'])
            
            # 5. Push to Calendar
            print("Pushing workouts to Google Calendar...")
            cal_service = calendar_manager.get_calendar_service()
            if cal_service:
                user_calendar_id = user_profile.get('calendar_id', recipient) 
                
                for day_name, exercises in weekly_workout_data.items():
                    if day_name == 'coaching_notes' or not isinstance(exercises, list):
                        continue
                    # Create a summary of exercises for the description
                    ex_list = "\n".join([f"- {ex.get('exercise', 'Exercise')} ({ex.get('sets', 3)}x{ex.get('reps', '10')})" for ex in exercises])
                    calendar_manager.create_workout_event(cal_service, day_name, ex_list, user_calendar_id)
            
            # 6. Log to Google Sheet (pass None for phase since AI decides per-exercise)
            sheet_manager.log_week_to_sheet(
                user_profile.get('google_sheet_name', 'My Workout Plan'),
                weekly_workout_data,
                user_profile['current_week'],
                None,  # No fixed phase - AI decides per exercise
                user_profile
            )

            # 7. Export Dashboard Data (JSON for web dashboard)
            print("Exporting dashboard data...")
            dashboard_exporter.export_dashboard_data(weekly_workout_data, user_profile)

            # 8. Increment Week
            update_week(user_profile)
            print("Week updated. Process complete.")
        else:
            print("Failed to generate weekly plan data.")

