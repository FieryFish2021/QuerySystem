# Slack channel:
# http://pythoniiprojects.slack.com

############################################
# Trying to send email with python
# Reference: https://stackoverflow.com/questions/64505/sending-mail-from-python-using-smtp
# https://www.tutorialandexample.com/flask-email-verification/
# TODO: We need a to register a new email
def sendEmail():
  SMTPserver = 'smtp.att.yahoo.com'
  sender =     'me@my_email_domain.net'
  destination = ['recipient@her_email_domain.com']
  
  USERNAME = "USER_NAME_FOR_INTERNET_SERVICE_PROVIDER"
  PASSWORD = "PASSWORD_INTERNET_SERVICE_PROVIDER"
  
  # typical values for text_subtype are plain, html, xml
  text_subtype = 'plain'
  
  content="""\
  Test message
  """ 
  
  subject="Sent from Python"
  
  import sys, os, re
  
  from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
  # from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)
  
  # old version
  # from email.MIMEText import MIMEText
  from email.mime.text import MIMEText
  
  try:
      msg = MIMEText(content, text_subtype)
      msg['Subject']=       subject
      msg['From']   = sender # some SMTP servers will do this automatically, not all
  
      conn = SMTP(SMTPserver)
      conn.set_debuglevel(False)
      conn.login(USERNAME, PASSWORD)
      try:
          conn.sendmail(sender, destination, msg.as_string())
      finally:
          conn.quit()
  
  except:
      print( "mail failed; %s" % "CUSTOM_ERROR" ) # give an error message

############################################

from flask import Flask, render_template, request, session, redirect, url_for
import os, datetime
from replit import db


# Functions that deal with the SQL database
import sqlite3
import sqlalchemy as sa 


"""
# the next lines create the table with the data type for each column
USERS_curs.execute('''CREATE TABLE users
    (user_id VARCHAR(20) PRIMARY KEY,
    age INT)''')
"""

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

# Print database contents to console for debugging
print('\nRESOLVED QUESTIONS:')
print(db['DATABASE_RESOLVED_QUESTIONS'])
print('\nUNRESOLVED QUESTIONS:')
print(db['DATABASE_QUESTIONS'])
print('\nCRENDENTIALS:')
print(db["DATABASE_LOGIN_CREDENTIALS"])


web_site = Flask(__name__)
web_site.secret_key = 'SuperDuperSecureSecretKey'

########################################################
############## 1. Question Logging System ##############
########################################################

# The first page the user will see
@web_site.route('/')
def index():
  # Check if the user is logged in. If yes, show them the main page.
  if 'loggedin' in session:
      return render_template('index.html')
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
    # TODO: Collect the tag and save in a variable
    name = request.form['name']
    timedate = str(datetime.datetime.now()).split('.')[0]
    status = False
    #email = session['email'] # [?] For some reason, this doesn't work
    # Asking the user to enter name might be unnecessary since we could just collect their email
    
    # Save them to the repl database as a LIST
    # Note: maybe Object oriented programming would work better than a list?
    db['DATABASE_QUESTIONS'].append([name,question,timedate,status])
  return render_template('index.html',message = message) 
#	return '%s Question Submitted <br/> <a href="/">Back Home</a>' % (db.keys())
	
# Note: the function names are confusing. Should probably change them sometimes.
# TODO: Make a RESOLVE/REMOVE button for each question
# Display all Unresolved Questions in a HTML table
@web_site.route('/all_questions', methods=['GET'])
def all_questions(message = "Unresolved questions will be displayed here."):
  link = '/view_resolved_questions'
  linktext = 'View resolved questions'
  return render_template('all_questions.html',keys=db['DATABASE_QUESTIONS'], message = message, link=link, linktext = linktext)

# Display all resolved questions
@web_site.route('/view_resolved_questions', methods=['POST','GET'])
def view_resolved_questions():
  message = "Resolved questions will be displayed here."
  link = '/all_questions'
  linktext = 'View unresolved questions'
  return render_template('all_questions.html',keys=db['DATABASE_RESOLVED_QUESTIONS'], message = message, link = link, linktext = linktext)

# Display a SINGLE Question
# The function name is confusing, should change it to something like "view_a_single_question"
@web_site.route('/view_questions', methods=['POST','GET'])
def view_questions():
  if len(db['DATABASE_QUESTIONS'])==0:
   return all_questions(message = "No more questions for now!")
  
  question = db['DATABASE_QUESTIONS'][0][1]
  question_data = db['DATABASE_QUESTIONS'][0][0]
  return render_template('view_questions.html',data=question_data,question=question)

# Mark the current question as resolved and display the next question
@web_site.route('/resolve_question', methods=['POST','GET'])
def resolve_question():
  if request.form['question']:
    question = request.form['question']
    print(question)
    return all_questions()
  # Set the question status to True/Resolved
  db['DATABASE_QUESTIONS'][0][3] = True
  
  # Move the resolved question to another database
  db['DATABASE_RESOLVED_QUESTIONS'].append(db['DATABASE_QUESTIONS'][0])
  del db['DATABASE_QUESTIONS'][0]
  
  return view_questions()

########################################################
############ 2. User Authentication System #############
########################################################
# https://codeshack.io/login-system-python-flask-mysql/
# https://pythonspot.com/login-authentication-with-flask/

# Sumedh's user authentication project
# https://deepnote.com/project/Mod-4-Project-B5e9E0XnQMOY5QMg57K_Kw/%2Fnotebook.ipynb

# Bootstap template by Jade
# https://replit.com/join/whbyrcav-greenmario1 

@web_site.route('/signup',methods=['POST','GET'])
def signup():
  return render_template('signup.html')

# Hanlle sign up request
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
  if 'loggedin' in session:
    message = "You are already logged in!"
    return render_template('logout.html',message=message)
  return render_template('login.html',)

@web_site.route('/logout',methods=['POST','GET'])
def logout():
  # Remove session data, this will log the user out
  session.pop('loggedin', None)
  session.pop('email', None)
  message = "You are currently logged out!"
  return render_template('login.html', message = message)

# Handle login attempt
@web_site.route('/password_check',methods=['POST','GET'])
def password_check():
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
    return render_template('index.html',message = message)
  else:
    message = 'Incorrect password!'
  return render_template('login.html',message = message)
  

if __name__ == '__main__':
	web_site.run(host='0.0.0.0', port=3001)