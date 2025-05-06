import tkinter as tk
from tkinter import messagebox
import sqlite3

# 🔹 Connect to SQLite database (creates one if not found)
conn = sqlite3.connect("todo.db")
cursor = conn.cursor()

# 🔹 Create the tasks table if it doesn't exist
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)")
conn.commit()

# Function to load tasks from database
def load_tasks():
    cursor.execute("SELECT task FROM tasks")
    return [row[0] for row in cursor.fetchall()]

# Function to add task to database
def add_task():
    task = task_entry.get()
    if task:
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
        task_list.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task!")

# Function to remove task from database
def remove_task():
    selected_task = task_list.curselection()
    if selected_task:
        task = task_list.get(selected_task)
        cursor.execute("DELETE FROM tasks WHERE task = ?", (task,))
        conn.commit()
        task_list.delete(selected_task)
    else:
        messagebox.showwarning("Warning", "Select a task to remove!")

# 🔹 Load existing tasks when the app starts
tasks = load_tasks()

# Tkinter GUI Setup
root = tk.Tk()
root.title("To-Do List")

task_entry = tk.Entry(root, width=30)
task_entry.pack(pady=10)

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack()

remove_button = tk.Button(root, text="Remove Task", command=remove_task)
remove_button.pack()

task_list = tk.Listbox(root, width=50, height=10)
task_list.pack(pady=10)

# 🔹 Load saved tasks into the Listbox
for task in tasks:
    task_list.insert(tk.END, task)

# Run the Tkinter app
root.mainloop()