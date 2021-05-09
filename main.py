from flask import Flask, render_template, request
import os
from replit import db

web_site = Flask(__name__)

#https://www.freecodecamp.org/news/connect-python-with-sql/

def clear_database():
  for key in db.keys():
    del db[key]

@web_site.route('/')
def index():
	return render_template('index.html')


@web_site.route('/all_questions', methods=['GET'])
def all_questions():
	return render_template('all_questions.html',keys=db.keys())


@web_site.route('/question', methods=['POST'])
def question():
	name = request.form['name']
	question = request.form['question']
	'''
	f = open('questions.log', 'a')
	f.write(question + ':' + name)
	f.write('\n')
	f.close()
	'''
	db[question] = name
	for key in db.keys():
	   print(db[key])
	return '%s Question Submitted <br/> <a href="/">Back Home</a>' % (db.keys())

@web_site.route('/answer', methods=['POST','GET'])
def answer():
  if len(list(db.keys()))==0:
    return render_template('no_questions.html')
  question = list(db.keys())[0]
  print(question)
  question_data = db[question]
  return render_template('answer.html',data=question_data,question=question)


@web_site.route('/next_question')
def next_question():
  
  question = list(db.keys())[0]
  del db[question]
  
  return answer()


if __name__ == '__main__':
	web_site.run(host='0.0.0.0', port=3001)
