from flask import Flask, request, render_template, session
import re
import sqlite3
from frontend import app

#Establish connection/cursor, create database (leaving this code here just for ease of addition in the future)
"""
conn = sqlite3.connect('frontend/Backend/userdata.db')
c = conn.cursor()
c.execute("CREATE TABLE userdata (email TEXT,password TEXT);")
conn.commit()
conn.close()
"""

logged = False
current_user = None

# Route user to the proper page 
@app.route('/')
def home():
    return render_template('landing.html', logged_in=logged)

@app.route('/landing.html')
def landing():
    return render_template('landing.html', logged_in=logged)

@app.route('/logged_out.html')
def log_out():
    logged, current_user=False, None
    return render_template('landing.html', logged_in=False)

@app.route('/calculator.html')
def calculator_page():
    return render_template('calculator.html', logged_in=logged)

@app.route('/login.html')
def login_page():
    return render_template('login.html', logged_in=logged)

@app.route('/signup.html')
def signup_page():
    return render_template('signup.html', logged_in=logged)

@app.route('/logger.html')
def logger_page():
    if not logged: return render_template('signup.html', show_error=True, error_message="Signup to use logger")
    return render_template('logger.html')

@app.route('/sources.html')
def sources_page():
    return render_template('sources.html', logged_in=logged)

@app.route('/stats.html')
def stats_page():
    if not logged: return render_template('signup.html', show_error=True, error_message="Signup to see stats")
    return render_template('stats.html')

@app.route('/tasks.html')
def tasks_page():
    return render_template('tasks.html', logged_in=logged)

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['pass']
    password2 = request.form['confirm-pass']

    if not valid_email(email):
        return render_template('signup.html', show_error=True, error_message='Email is invalid')
    
    conn = sqlite3.connect('frontend/Backend/userdata.db')
    c = conn.cursor()

    c.execute("SELECT * FROM userdata WHERE email=?", (email,))
    row = c.fetchone()

    if password != password2: 
        return render_template('signup.html', show_error=True, error_message='Passwords do not match')

    elif row is None: #email doesn't exist yet
        c.execute(f"INSERT INTO userdata (email, password) VALUES ('{email}', '{password}');")
        conn.commit()
        conn.close()
        current_user, logged = email, True
        return render_template('landing.html', logged_in=True)  

    conn.close()
    return render_template('signup.html', show_error=True, error_message='Email already exists')
        
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['pass']

    if not valid_email(email):
        return render_template('login.html', show_error=True, error_message='Email is invalid')

    conn = sqlite3.connect('frontend/Backend/userdata.db')
    c = conn.cursor()
    c.execute("SELECT * FROM userdata WHERE email=?", (email,))
    row = c.fetchone()

    if row is None: #email doesn't exist
        conn.close()
        return render_template('login.html', show_error=True, error_message='Email does not exist')
    elif row[1] == password: # password matches
        conn.close()
        current_user, logged = email, True
        return render_template('landing.html', logged_in=True)  

    else: # password doesn't match (duh)
        conn.close()
        return render_template('login.html', show_error=True, error_message='Password is incorrect')
  
def printuserdata():
    conn = sqlite3.connect('frontend/Backend/userdata.db')
    c = conn.cursor()
    c.execute("DELETE FROM userdata")
    c.execute('SELECT * FROM userdata')
    rows = c.fetchall()
    for row in rows:
        print(row)
    conn.close()

def valid_email(email):
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(regex, email)
