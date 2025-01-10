import os
import pandas as pd
from datetime import datetime

# Create the attendance file if it doesn't exist
def create_attendance_file(attendance_file):
    if not os.path.exists(attendance_file):
        with open(attendance_file, 'w') as f:
            f.write('Enrollment,Name,Date,Time\n')

# Save attendance to the file
def save_attendance(enrollment, name):
    with open('attendance.csv', 'a') as f:
        f.write(f"{enrollment},{name},{datetime.now().date()},{datetime.now().strftime('%H:%M:%S')}\n")

# Load attendance from the file
def load_attendance(attendance_file):
    if os.path.exists(attendance_file):
        return pd.read_csv(attendance_file)
    return pd.DataFrame()
