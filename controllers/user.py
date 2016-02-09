from flask import *
from objects.User import User
import extensions
import re
''' This controller handles the /user urls, mainly dealing with creation and deletion of user accounts '''

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/user', methods=['GET', 'POST'])
def user_route():
	error_message = []
	if 'username' in session:
		return redirect(url_for('user.user_edit_route'))
	if request.method == 'POST':
		if request.form['password1'] != request.form['password2']:
			error_message.append('Passwords do not match')
		user = User(request.form['username'],
			request.form['firstname'],
			request.form['lastname'],
			request.form['password1'],
			request.form['email'])
		error_message = error_message + user.validate()
		temp_user = extensions.get_user(request.form['username'])
		if temp_user != None:
			error_message.append('This username is taken')
		if error_message == []:
			user.create_salt()
			user.hash_pass()
			extensions.add_user(user)
			if 'username' in session:
				return redirect(url_for('user.user_edit_route'))
			else:
				return redirect(url_for('index.login_route'))

    	return render_template('user.html', error_mess = error_message) 

@user.route('/user/edit', methods=['GET', 'POST'])
def user_edit_route():
	error_message = []
	message = []
	if 'username' not in session:
		return redirect(url_for('index.login_route') + '?url=' + url_for('user.user_edit_route'))
	username = session['username']
	this_user = extensions.get_user(username)
	if request.method == 'POST':
		if 'password1' and 'password2' in request.form:
			if (request.form['password1'] != request.form['password2']):
				error_message.append('Passwords do not match')
			elif request.form['password1'] != '':
				if not re.match('^[A-Za-z0-9_]*$', request.form['password1']):
					message.append('Passwords may only contain letters, digits, and underscores')
				if not re.match('^(?=.*[a-zA-Z])(?=.*\d).+$', request.form['password1']):
					message.append('Passwords must contain at least one letter and one number')
				this_user.set_password(request.form['password1'])
		if 'firstname' in request.form:
			if request.form['firstname'] != '':
				if len(request.form['firstname']) > 20:
					message.append('Firstname must be no longer than 20 characters')
				this_user.set_firstname(request.form['firstname'])
		if 'lastname' in request.form:
			if request.form['lastname'] != '':
				if len(request.form['lastname']) > 20:
					message.append('Lastname must be no longer than 20 characters')
				this_user.set_lastname(request.form['lastname']);
		if 'email' in request.form:
			if request.form['email'] != '':
				if not re.match('[^@]+@[^@]+\.[^@]+', self.__email):
					message.append('Email address must be valid')
				this_user.set_email(request.form['email']);
		# needed because error_message can be changed with not matching passwords
		error_message = message
		if error_message == []:
			this_user.create_salt()
			this_user.hash_pass()
			extensions.update_user(this_user)
		
	return render_template('user_edit.html',error_mess = error_message, user = extensions.get_user(username))



