from flask import Flask, jsonify, render_template
import sqlite3
import random

app = Flask(__name__)

# Database connection function
def connect_db():
    return sqlite3.connect('projects.db')

# Initialize the database and create the table
def init_db():
    conn = connect_db()
    cursor = conn.cursor()

    # Drop the table if it already exists (to recreate it)
    cursor.execute("DROP TABLE IF EXISTS projects")

    # Create the table with the required columns
    cursor.execute("""
        CREATE TABLE projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT NOT NULL,
            progress INTEGER NOT NULL,
            deadline TEXT NOT NULL,
            teamMembers TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# Insert sample data into the database
def insert_sample_data():
    conn = connect_db()
    cursor = conn.cursor()

    projects = [
        ('Building a Hospital', 'In Progress', 40, '2024-12-31', 'John, Sarah, Mike'),
        ('School Construction', 'Not Started', 0, '2025-05-15', 'Alice, Bob'),
        ('Bridge Over River', 'Completed', 100, '2024-07-15', 'Dave, Rachel'),
        ('Highway Extension', 'In Progress', 60, '2025-01-01', 'Steve, Anna, Tom'),
        ('Office Complex', 'Not Started', 0, '2025-06-01', 'Paul, Katie'),
    ]

    cursor.executemany("""
        INSERT INTO projects (name, status, progress, deadline, teamMembers)
        VALUES (?, ?, ?, ?, ?)
    """, projects)

    conn.commit()
    conn.close()

# Homepage route
@app.route('/')
def home():
    return render_template('index.html')  # Make sure you create this file in templates/

# API route to get all projects
@app.route('/api/projects')
def get_projects():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()
    conn.close()

    project_data = [{
        'id': row[0],
        'name': row[1],
        'status': row[2],
        'progress': row[3],
        'deadline': row[4],
        'teamMembers': row[5].split(', ')
    } for row in projects]

    return jsonify(project_data)

# Run the app
if __name__ == "__main__":
    init_db()  # Initialize the database with schema
    insert_sample_data()  # Add sample data
    app.run(debug=True)  # ✅ This line was broken earlier — now fixed!

