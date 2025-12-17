import visualizer
import base64

mock_data = [
    {'Date': '2023-10-01', 'Exercise': 'Barbell Hip Thrust', 'Weight': '135 lbs'},
    {'Date': '2023-10-08', 'Exercise': 'Barbell Hip Thrust', 'Weight': '145 lbs'},
    {'Date': '2023-10-15', 'Exercise': 'Barbell Hip Thrust', 'Weight': '155 lbs'},
    {'Date': '2023-10-01', 'Exercise': 'Smith Machine Squat', 'Weight': '95 lbs'},
    {'Date': '2023-10-08', 'Exercise': 'Smith Machine Squat', 'Weight': '100 lbs'},
]

try:
    chart_base64 = visualizer.generate_progress_chart(mock_data)
    if chart_base64:
        print("Success: Chart generated.")
        # print(f"Base64 length: {len(chart_base64)}")
    else:
        print("Failure: No chart generated.")
except Exception as e:
    print(f"Error: {e}")
