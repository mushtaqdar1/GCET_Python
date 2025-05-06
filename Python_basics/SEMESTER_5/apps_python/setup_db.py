import sqlite3
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

conn = sqlite3.connect("attendance.db")
cursor = conn.cursor()

# Create a new hashed password for admin
new_password_hash = bcrypt.generate_password_hash("newpassword").decode("utf-8")

cursor.execute("UPDATE users SET password = ? WHERE username = ?", (new_password_hash, "admin"))
conn.commit()
conn.close()

print("Admin password reset successfully! New password: newpassword")