from flask import *
from objects.User import User
import extensions
import re
''' This controller handles the /user urls, mainly dealing with creation and deletion of user accounts '''

user = Blueprint('user', __name__, template_folder='templates')

@user.route('/api/v1/user', methods=['GET', 'POST'])
def user_api():
	username = ''
	if request.method == 'POST':
		errors = []
		req = request.get_json(force=True)
		if req['password1'] != req['password2']:
			errors.append('Passwords do not match')
		user = User(req['username'],
			req['firstname'],
			req['lastname'],
			req['password1'],
			req['email'])
		errors = errors + user.validate()
		temp_user = extensions.get_user(req['username'])
		if temp_user != None:
			errors.append('This username is taken')
		print errors
		if errors != []:
			print 'Should return json errors'
			error_dict = {}
			error_dict['errors'] = errors
			return jsonify(error_dict)
		user.create_salt()
		user.hash_pass()
		extensions.add_user(user)
		username = req['username']
	if username == '':
		if 'username' not in session:
			abort(403)
		username = session['username']
	user = extensions.get_user(username)
	response = {}
	response['username'] = user.get_username()
	response['firstname'] = user.get_firstname()
	response['lastname'] = user.get_lastname()
	response['email'] = user.get_email()
	return jsonify(response)
	

@user.route('/user', methods=['GET'])
def user_route():
    	return render_template('user.html', error_mess = []) 

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



