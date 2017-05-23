from flask import Flask, url_for, render_template, request, redirect
from werkzeug.utils import secure_filename

from flask import jsonify

import database

from database import db

from database import Phonebook

import random



app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def hello_world():
	return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])	
def login():
	if request.method == 'POST':
		f = request.files['file']
		f.save('/Users/aman/Desktop/' + secure_filename(f.filename))
		return render_template('welcome.html', name = request.form['username'], password = request.form['password'])
	
	return render_template('login.html')


@app.route('/images', methods=['POST', 'GET'])
def randImages():
	# Says Hi to the user
	if request.method == 'POST':
		return getRandImages()

	return render_template('images.html')


@app.route('/imagesJS', methods=['GET'])
def randomImages():	
	return render_template('imagesAjax.html')


@app.route('/api/rand-images', methods=['GET'])
def getImages():	
	return generateRandomImages()


@app.route('/phonebook', methods=['GET', 'POST'])
def phonebook():
	if request.method == 'POST':
		name = request.form['name']
		phoneNum = request.form['phone']

		dbEntry = Phonebook(name, phoneNum)
		db.session.add(dbEntry)
		db.session.commit()

		phoneList = Phonebook.query.all()

		return render_template('phonebook.html', message = 'Contact for '+name+' added.', phoneList = phoneList)

	else:
		phoneList = Phonebook.query.all()
		return render_template('phonebook.html', phoneList = phoneList)


@app.route('/phonebook/<int:id>', methods=['GET', 'POST'])
def editPhonebook(id):
	if request.method == 'POST':

		name = request.form['name']
		phoneNum = request.form['phone']
		
		entry = Phonebook.query.filter(Phonebook.id == id).first()
		entry.name = name
		entry.phone = phoneNum

		db.session.commit()

		phoneList = Phonebook.query.all()

		return render_template('phonebook.html', message = 'Contact deleted.', phoneList = phoneList)


	else:
		entry = Phonebook.query.filter(Phonebook.id == id).first()
		return render_template('edit-phonebook.html', entry = entry)


@app.route('/deletePhonebook/<int:id>', methods=['POST'])
def deletePhonebook(id):
	if request.method == 'POST':
		
		Phonebook.query.filter(Phonebook.id == id).delete()
		db.session.commit()

		return redirect(url_for('phonebook'))



images = ['file1', 'file2', 'file3', 'file4', 'file5', 'file6', 'file7']

# Custom Functions

def getRandImages():
	randImages = random.sample(images, 3)
	return render_template('images.html', images=randImages)


def generateRandomImages():
	randImages = random.sample(images, 3)
	newImages = []		
	for image in randImages:
		newImages.append(url_for('static', filename='randImages/'+image+'.png'))

	return jsonify(newImages)




# print("App Started")


if __name__ == '__main__':	
	print("App Started")
	app.run(debug=True)
	database.initialize()
# 	print("DB initializing")
# 	database.create_all()
