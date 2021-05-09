from flask import Flask, render_template, request
import os
#from replit import db
import replit

web_site = Flask(__name__)

#https://www.freecodecamp.org/news/connect-python-with-sql/


@web_site.route('/')
def index():
	return render_template('index.html')


@web_site.route('/hello', methods=['POST'])
def hello():
	name = request.form['name']
	question = request.form['question']
	#questions.append(question)
	print(os.listdir())
	f = open('questions.log', 'a')
	f.write(question + ':' + name)
	f.write('\n')
	f.close()

	return '%s Question Submitted <br/> <a href="/">Back Home</a>' % (question)


if __name__ == '__main__':
	web_site.run(host='0.0.0.0', port=3001)
