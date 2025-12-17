import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import io
import base64

def generate_progress_chart(data, exercises_to_plot=["Barbell Hip Thrust", "Smith Machine Squat", "Romanian Deadlift"]):
    """
    Generates a progress chart for specific exercises.
    Returns a base64 encoded image string to embed in HTML.
    """
    if not data:
        return None

    plt.figure(figsize=(10, 6))
    
    # Organize data by exercise
    # Assumes data has 'Date', 'Exercise', 'Weight' (cleaned)
    # We need to parse the 'Weight' string (e.g., "135 lbs") to a number
    
    plot_data = {ex: {'dates': [], 'weights': []} for ex in exercises_to_plot}
    
    for entry in data:
        ex_name = entry.get('Exercise')
        weight_str = str(entry.get('Weight', '0'))
        date_str = str(entry.get('Date', ''))
        
        if ex_name in exercises_to_plot and weight_str and date_str:
            try:
                # Clean weight string
                weight = float(''.join(filter(str.isdigit, weight_str)))
                # Parse date (Assuming format YYYY-MM-DD or similar, adjust as needed)
                # If date is missing/invalid, we might skip or use index
                # For simplicity in this v1, let's just use sequential index if date fails
                plot_data[ex_name]['weights'].append(weight)
                plot_data[ex_name]['dates'].append(date_str)
            except ValueError:
                continue

    # Plotting
    has_data = False
    for ex, values in plot_data.items():
        if values['weights']:
            plt.plot(values['weights'], marker='o', label=ex)
            has_data = True

    if not has_data:
        return None

    plt.title('Strength Progress (Key Lifts)')
    plt.xlabel('Sessions')
    plt.ylabel('Weight (lbs)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return image_base64
