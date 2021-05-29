# Slack channel:
# http://pythoniiprojects.slack.com

# Sumedh's user authentication project
# https://deepnote.com/project/Mod-4-Project-B5e9E0XnQMOY5QMg57K_Kw/%2Fnotebook.ipynb

# Bootstap stuff by Jade
# https://replit.com/join/whbyrcav-greenmario1 

from flask import Flask, render_template, request, session, redirect, url_for
import os, datetime
from replit import db


"""
# the next lines create the table with the data type for each column
USERS_curs.execute('''CREATE TABLE users
    (user_id VARCHAR(20) PRIMARY KEY,
    age INT)''')
"""

# Functions that deal with the SQL database
import sqlite3
import sqlalchemy as sa 
def add_user_to_database(email,password):
  USERS = sqlite3.connect('users.db')
  USERS_curs = USERS.cursor()
  ins = 'INSERT INTO users (user, password) VALUES(?,?)'
  USERS.execute(ins,(email,password))
  print("[*] User list:",get_database())
  USERS.commit()
  print("[*]",email,password,"added to database.")

def get_database(database='users.db',payload='SELECT user FROM users'):
  conn = sqlite3.connect(database)
  curs = conn.cursor()
  curs.execute(payload)
  rows = curs.fetchall()
  #print(rows)
  return rows

def get_userlist():
  user_list = get_database(database='users.db',payload='SELECT user FROM users')
  user_list = [user[0] for user in user_list]
  return user_list

'''

#print(get_userlist())
#print(get_database(payload='SELECT user, password FROM users'))
# Initializing variables and database

def clear_database():
  for key in db.keys():
    del db[key]
  # INITIALIZE the databases
  db['DATABASE_QUESTIONS']=[]
  db['DATABASE_LOGIN_CREDENTIALS']={}
  db['DATABASE_RESOLVED_QUESTIONS'] = []

clear_database()
print(db["DATABASE_QUESTIONS"])

print(db["DATABASE_RESOLVED_QUESTIONS"])
'''

web_site = Flask(__name__)
web_site.secret_key = 'SuperDuperSecureSecretKey'


print('\nRESOLVED QUESTIONS:')
print(db['DATABASE_RESOLVED_QUESTIONS'])
print('\nUNRESOLVED QUESTIONS:')
print(db['DATABASE_QUESTIONS'])
print('\nCRENDENTIALS:')

print(db["DATABASE_LOGIN_CREDENTIALS"])

########################################################
############## 1. Question Logging System ##############
########################################################

# The first page the user will see
@web_site.route('/')
def index():
  # Check if the user is logged in. If yes, show them the main page.
  if 'loggedin' in session:
      return render_template('index.html', email=session['email'])
  else:
    # If the user is not logged in, redirect to the login page
    message = "To submit a question, please first login!"
    # This returns the rendered login.html page and passes the message string to the frontend.
    return render_template('login.html', message = message)


@web_site.route('/submit_question', methods=['POST'])
def submit_question():
  question = request.form['question']
  # Check if the input is empty
  if question=='':
    message = "Please enter something!"
  else:
    message = "Your question has been submitted!"
    # Get user inputs
    # Note: Asking the user to enter name might be unnecessary since we could just collect their email
    #email = session['email'] # [?] For some reason, this doesn't work
    # TODO: Collect the tag and save in a variable
    name = request.form['name']
    timedate = str(datetime.datetime.now()).split('.')[0]
    status = False
    # Save them to the repl database as a LIST
    # Note: maybe Object oriented programming would work better than a list?
    db['DATABASE_QUESTIONS'].append([name,question,timedate,status])
  return render_template('index.html',message = message) 
#	return '%s Question Submitted <br/> <a href="/">Back Home</a>' % (db.keys())
	
# Display a Single Question
@web_site.route('/view_questions', methods=['POST','GET'])
def view_questions():
  if len(db['DATABASE_QUESTIONS'])==0:
    return render_template('no_questions.html')
  question = db['DATABASE_QUESTIONS'][0][1]
  question_data = db['DATABASE_QUESTIONS'][0][0]
  print(question)
  return render_template('view_questions.html',data=question_data,question=question)

# Display the Next Question
@web_site.route('/resolve_question')
def next_question():
  db['DATABASE_QUESTIONS'][0][3] = True
  db['DATABASE_RESOLVED_QUESTIONS'].append(db['DATABASE_QUESTIONS'][0])
  del db['DATABASE_QUESTIONS'][0]
  return view_questions()

########################################################
############ 2. User Authentication System #############
########################################################
# https://codeshack.io/login-system-python-flask-mysql/
@web_site.route('/signup',methods=['POST','GET'])
def signup():
  return render_template('signup.html')

@web_site.route('/create_new_account',methods=['POST','GET'])
def create_new_account():
  # Get user inputs
  password = request.form['password']
  email = request.form['email']
  
  # Check if the email exists in the dicionary.
  # If it exists, set the message to an error message.
  #if email in db["DATABASE_LOGIN_CREDENTIALS"]: # repl database
  if email in get_userlist(): # SQL database
    message = "That email address is taken."
  else:
  #  db["DATABASE_LOGIN_CREDENTIALS"][email]=password # Add to the repl database
    # If it doesn't exist, add a new user account.
    add_user_to_database(email,password) #Add to the SQL database
    message = "Account created successfully! Please login."
    return render_template('login.html',message = message) 
  return render_template('signup.html',message = message) # Pass the error/success message to the front end

@web_site.route('/login',methods=['POST','GET'])
def login():
  return render_template('login.html')


# Handle login attempt
# https://pythonspot.com/login-authentication-with-flask/
@web_site.route('/password_check',methods=['POST','GET'])
def password_check():
  session['email'] = 'N/A'
  # Get user inputs
  password = request.form['password']
  email = request.form['email']
  print("[*] Repl Database:",db["DATABASE_LOGIN_CREDENTIALS"])
  print("[*] SQL database:",get_database(payload="SELECT * FROM users"))
  
  # Check to see if the email exists in the database
  # If it exists, check to see if the password matches
  #if not(email in db["DATABASE_LOGIN_CREDENTIALS"]):
  if not (email in get_userlist()):
    message = 'Email not found!'
  #elif password == db["DATABASE_LOGIN_CREDENTIALS"][email]:
  elif (email, password,) in get_database(payload="SELECT * FROM users"):
    message = 'Login successful! Welcome, '+email+'!'
    # TODO: Do stuff here for a successful login attempt
    # Only a logged in user could post questions
    session['loggedin'] = True
    session['email'] = email
    return render_template('index.html',message = message, email = session['email'])
  else:
    message = 'Incorrect password!'
  return render_template('login.html',message = message, email = session['email'])
  

# Display All Questions in a HTML table
# TODO: Make a RESOLVE/REMOVE button for each question
@web_site.route('/all_questions', methods=['GET'])
def all_questions():
  return render_template('all_questions.html',keys=db['DATABASE_QUESTIONS'])
  

if __name__ == '__main__':
	web_site.run(host='0.0.0.0', port=3001)