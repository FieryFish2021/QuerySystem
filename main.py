
from flask import Flask, render_template, request
import os
from replit import db

web_site = Flask(__name__)

@web_site.route('/')
def index():
	return render_template('index.html')

# TODO: The login & sign up system
# https://pythonspot.com/login-authentication-with-flask/

def clear_database():
  for key in db.keys():
    del db[key]
  # INITIALIZE the databases
  db['DATABASE_QUESTIONS']=[]
  db['DATABASE_LOGIN_CREDENTIALS']={}

#clear_database()

print(db["DATABASE_QUESTIONS"])
print(db["DATABASE_LOGIN_CREDENTIALS"])

@web_site.route('/signup',methods=['POST','GET'])
def signup():
  return render_template('signup.html')

# Hello

@web_site.route('/create_new_account',methods=['POST','GET'])
def create_new_account():
  password = request.form['password']
  email = request.form['email']
  db["DATABASE_LOGIN_CREDENTIALS"][email]=password
  return '%s Account Created! <br/> <a href="/">Back Home</a>' % (db["DATABASE_LOGIN_CREDENTIALS"])
#return render_template('signup.html')


@web_site.route('/login',methods=['POST','GET'])
def login():
  return render_template('login.html')
  

# ------------ Log a Question ------------
@web_site.route('/submit_question', methods=['POST'])
def question():
	name = request.form['name']
	question = request.form['question']
	
	# Log the quesiton and the name to the repl database.
	# TODO: Log other infomation as well:
	# 1. ALL students who asked the question (stored in a list)
	# 2. The current date/time (requires the datetime module)
	# 3. Resolved or not (a Boolean value, True/False)
	
	# The quesiton should be the KEY,
	# all the other information should be stored in a LIST,
	# and the list will be the VALUE.
	# db[question] = [[name1,name2],date_time,resolved]
	
	db['DATABASE_QUESTIONS'].append([name,question])
	for key in db.keys():
	   print(db[key])
	return '%s Question Submitted <br/> <a href="/">Back Home</a>' % (db.keys())


# ------------ Display a Single Question ------------
@web_site.route('/answer', methods=['POST','GET'])
def answer():
  if len(db['DATABASE_QUESTIONS'])==0:
    return render_template('no_questions.html')
  question = db['DATABASE_QUESTIONS'][0][1]
  print(['DATABASE_QUESTIONS'][0])
  question_data = db['DATABASE_QUESTIONS'][0][0]
  return render_template('answer.html',data=question_data,question=question)



# ------------ Display the Next Question ------------
@web_site.route('/resolve_question')
def next_question():
  
  print(db['DATABASE_QUESTIONS'][0])
  # DELETE the previous question
  # TODO: find a way to ARCHIVE the resolved questions,
  #       instead of DELETING them
  del db['DATABASE_QUESTIONS'][0]
  return answer()

# ------------ Display All Questions ------------
@web_site.route('/all_questions', methods=['GET'])
def all_questions():
	return render_template('all_questions.html',keys=db['DATABASE_QUESTIONS'])


if __name__ == '__main__':
	web_site.run(host='0.0.0.0', port=3001)

# Hello World
# Hello there!
# Hello world... Testing Pull Requests! 
