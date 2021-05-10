from flask import Flask, render_template, request
import os
from replit import db

web_site = Flask(__name__)

@web_site.route('/')
def index():
	return render_template('index.html')

# TODO: Finish the login & sign up system!
# Reference:
# https://pythonspot.com/login-authentication-with-flask/

# We need to store the password and email in our database.
# Since we don't have to worry about security,
# a dictionary might do the trick.

# The repl database is already used to store the questions,
# so it might be trickier to store pw/emails in the repl database.

@web_site.route('/signup',methods=['POST','GET'])
def signup():
  return render_template('signup.html')

@web_site.route('/login',methods=['POST','GET'])
def login():
  return render_template('login.html')
  

# ------------ Log a Question ------------
@web_site.route('/question', methods=['POST'])
def question():
	name = request.form['name']
	question = request.form['question']
	
	
	# Commented out because this method is too primitive.
	'''
	#f = open('questions.log', 'a')
	#f.write(question + ':' + name)
	#f.write('\n')
	#f.close()
	'''
	
	# Log the quesiton and the name to the repl database.
	# TODO: Log other infomation as well:
	# 1. ALL students who asked the question (stored in a list)
	# 2. The current date/time (requires the datetime module)
	# 3. Resolved or not (a Boolean value, True/False)
	
	# The quesiton should be the KEY,
	# all the other information should be stored in a LIST,
	# and the list will be the VALUE.
	# db[question] = [[name1,name2],date_time,resolved]
	
	db[question] = name
	for key in db.keys():
	   print(db[key])
	return '%s Question Submitted <br/> <a href="/">Back Home</a>' % (db.keys())


# ------------ Display a Single Question ------------
@web_site.route('/answer', methods=['POST','GET'])
def answer():
  if len(list(db.keys()))==0:
    return render_template('no_questions.html')
  question = list(db.keys())[0]
  print(question)
  question_data = db[question]
  return render_template('answer.html',data=question_data,question=question)



# ------------ Display the Next Question ------------
@web_site.route('/next_question')
def next_question():
  
  question = list(db.keys())[0]
  # DELETE the previous question
  # TODO: find a way to ARCHIVE the resolved questions,
  #       instead of DELETING them
  del db[question]
  
  return answer()

# ------------ Display All Questions ------------
@web_site.route('/all_questions', methods=['GET'])
def all_questions():
	return render_template('all_questions.html',keys=db.keys())


'''
def clear_database():
  for key in db.keys():
    del db[key]

'''

if __name__ == '__main__':
	web_site.run(host='0.0.0.0', port=3001)

# Hello World