# Simple To-Do List App
import sqlite3

# 🔹 Connect to the database (creates it if it doesn't exist)
conn = sqlite3.connect("todo.db")
cursor = conn.cursor()

# 🔹 Create a table for tasks (if it doesn't exist)
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)")
conn.commit()

# Function to load tasks from the database
def load_tasks():
    cursor.execute("SELECT task FROM tasks")
    return [row[0] for row in cursor.fetchall()]

# Function to add a task and store it in the database
def add_task(task):
    cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
    conn.commit()

# Function to remove a task
def remove_task(task):
    cursor.execute("DELETE FROM tasks WHERE task = ?", (task,))
    conn.commit()

# 🔹 Load existing tasks when the app starts
tasks = load_tasks()
print("Existing tasks:", tasks)
tasks = []

def show_tasks():
    print("\nYour To-Do List:")
    for index, task in enumerate(tasks, 1):
        print(f"{index}. {task}")

def add_task():
    task = input("Enter a new task: ")
    tasks.append(task)
    print(f"Task '{task}' added successfully!")

def remove_task():
    show_tasks()
    index = int(input("Enter the task number to remove: ")) - 1
    if 0 <= index < len(tasks):
        removed_task = tasks.pop(index)
        print(f"Task '{removed_task}' removed!")
    else:
        print("Invalid task number!")

while True:
    print("\nOptions: 1. Show Tasks  2. Add Task  3. Remove Task  4. Exit")
    choice = input("Choose an option: ")
    
    if choice == "1":
        show_tasks()
    elif choice == "2":
        add_task()
    elif choice == "3":
        remove_task()
    elif choice == "4":
        print("Exiting... Have a productive day!")
        break
    else:
        print("Invalid choice! Please try again.")