from flask import Flask, request, render_template, redirect, url_for, send_file, session
import sqlite3
import pandas as pd
import os
from fpdf import FPDF
from datetime import timedelta
from flask_session import Session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)  # Initialize Flask
app.secret_key = "your_secret_key"  # Change this to a secure key

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app) # Initialize Flask-Bcrypt       
# Initialize Flask app  
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secure key
app.config["UPLOAD_FOLDER"] = "uploads/"
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=10)

# Initialize session management & authentication
Session(app)
login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

# Ensure uploads folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Function to connect to database
def connect_db():
    return sqlite3.connect("attendance.db")

# Define User class for authentication
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return User(user[0], user[1])
    return None

# Home route
@app.route("/")
def home():
    return render_template("index.html")

# Register new user with hashed password
@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    bcrypt.generate_password_hash("admin").decode("utf-8")
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

    return "User registered successfully!"

# Login route with hashed password verification
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[2], password):
            login_user(User(user[0], user[1]))
            return redirect(url_for("dashboard"))
        else:
            return "Invalid username or password!"

    return render_template("login.html")

# Logout route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("login"))

# Dashboard route
@app.route("/dashboard")
@login_required
def dashboard():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    records = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", records=records)
# Bulk attendance upload (CSV/Excel)
@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload_attendance():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or file.filename == "":
            return "No file selected!"

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        try:
            df = pd.read_excel(filepath) if file.filename.endswith(".xlsx") else pd.read_csv(filepath)
            conn = connect_db()
            cursor = conn.cursor()

            for _, row in df.iterrows():
                cursor.execute(
                    "INSERT INTO attendance (date, name, roll_no, status) VALUES (?, ?, ?, ?)",
                    (row["Date"], row["Name"], row["Roll No"], row["Status"])
                )

            conn.commit()
            conn.close()
            return "Bulk attendance upload successful!"
        except Exception as e:
            return f"Error processing file: {str(e)}"

    return render_template("upload.html")

# Export attendance as Excel
@app.route("/export/excel")
@login_required
def export_excel():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    records = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(records, columns=["ID", "Date", "Name", "Roll No", "Status"])
    excel_file = "attendance_report.xlsx"
    df.to_excel(excel_file, index=False, engine="openpyxl")

    return send_file(excel_file, as_attachment=True)

# Export attendance as PDF
@app.route("/export/pdf")
@login_required
def export_pdf():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM attendance")
    records = cursor.fetchall()
    conn.close()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "Attendance Report", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    for record in records:
        pdf.cell(200, 10, f"{record[1]} | {record[2]} | {record[3]} | {record[4]}", ln=True)

    pdf_file = "attendance_report.pdf"
    pdf.output(pdf_file)

    return send_file(pdf_file, as_attachment=True)

# Start Flask app
if __name__ == "__main__":
    app.run(debug=True)

@app.route("/upload_attendance", methods=["POST"])
def upload_attendance():
    file = request.files["file"]
    df = pd.read_csv(file)
    conn = connect_db()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("INSERT INTO attendance (date, name, roll_no, status) VALUES (?, ?, ?, ?)", 
                       (row["Date"], row["Name"], row["Roll No"], row["Status"]))
    
    conn.commit()
    conn.close()
    return "Attendance uploaded successfully!"