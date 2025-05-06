import pandas as pd
import datetime

# Create a dictionary to store student data
attendance = {}

# Function to mark attendance
def mark_attendance(name, roll_no, status):
    date = datetime.date.today().strftime("%Y-%m-%d")
    if date not in attendance:
        attendance[date] = []
    attendance[date].append({"Name": name, "Roll No": roll_no, "Status": status})

# Function to export attendance to Excel
def export_to_excel():
    df = pd.DataFrame([{"Date": date, **record} for date, records in attendance.items() for record in records])
    df.to_excel("Student_Attendance.xlsx", index=False)
    print("Attendance saved to Excel!")

# Sample usage
mark_attendance("Mushtaq", "101", "Present")
mark_attendance("Ahmad", "102", "Absent")

export_to_excel()
import sqlite3

# Create or connect to a database
conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Create a table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        name TEXT,
        roll_no TEXT,
        status TEXT
    )
""")
conn.commit()

print("Database setup successfully!")

conn.close()