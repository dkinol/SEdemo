from flask import *
from objects.User import User
from controllers.support import generate_error_response, send_401, send_403
import extensions
import re
''' This controller handles the /user urls, mainly dealing with creation and deletion of user accounts '''

user = Blueprint('user', __name__, template_folder='templates')

def get_api_user_helper(username):
	user = extensions.get_user(username)
	response = {}
	response['username'] = user.get_username()
	response['firstname'] = user.get_firstname()
	response['lastname'] = user.get_lastname()
	response['email'] = user.get_email()
	return jsonify(response), 201

@user.route('/api/v1/user', methods=['GET', 'POST'])
def user_api():
	username = ''
        print 'got to func'
        print 'got hereereee'
	if request.method == 'POST':
	        req = request.get_json(force=True)
		errors = []
		if ('username' not in req) or ('firstname' not in req) or ('lastname' not in req) or ('email' not in req) or ('password1' not in req) or ('password2' not in req):
		    errors.append('You did not provide the necessary fields')
		    return jsonify(generate_error_response(errors)), 422
		if (req['username'] == '') or (req['email'] == '') or (req['password1'] == '') or (req['password2'] == ''):
		    errors.append('You did not provide the necessary fields')
		    return jsonify(generate_error_response(errors)), 422
		if req['password1'] != req['password2']:
			errors.append('Passwords do not match')
		user = User(req['username'], req['firstname'], req['lastname'], req['password1'], req['email'])
		errors = errors + user.validate()
		temp_user = extensions.get_user(req['username'])
		if temp_user != None:
			errors.append('This username is taken')
		if errors != []:
			return jsonify(generate_error_response(errors)), 422
		user.create_salt()
		user.hash_pass()
		extensions.add_user(user)
		username = req['username']
		if username == '':
			if 'username' not in session:
				return send_401()
                return get_api_user_helper(username)
        print "GOT HERE"
        if 'username' not in session:
            return send_401()
	username = session['username']
        return get_api_user_helper(username)
	

@user.route('/user', methods=['GET'])
def user_route():
    	return render_template('user.html', error_mess = []) 

@user.route('/api/v1/user', methods=['PUT'])
def user_edit_api():
	if 'username' not in session:
            return send_401()
	req = request.get_json(force=True)
	username = session['username']
	this_user = extensions.get_user(username)
        if (req['username'] != this_user.get_username()):
            return send_403()
	if ('username' not in req) or ('firstname' not in req) or ('lastname' not in req) or ('email' not in req) or ('password1' not in req) or ('password2' not in req):
            errors.append('You did not provide the necessary fields')
            return jsonify(generate_error_response(errors)), 422
	if (req['username'] == '') or (req['email'] == ''):
	        errors.append('You did not provide the necessary fields')
	        return jsonify(generate_error_response(errors)), 422
	errors = []
	if req['password1'] != req['password2']:
		errors.append('Passwords do not match')
	this_user.set_firstname(req['firstname'])
	this_user.set_lastname(req['lastname'])
	this_user.set_email(req['email'])
	if req['password1'] != '' and req['password2'] != '':
		print 'CHANGED PASSWORD'
		this_user.set_password(req['password1'])
	errors = errors + this_user.validate()
	if errors != []:
		return jsonify(generate_error_response(errors)), 422
	elif req['password1'] != '':
		this_user.create_salt()
		this_user.hash_pass()
	extensions.update_user(this_user)
	print 'will return now'
	return user_api()

@user.route('/user/edit', methods=['GET'])
def user_edit_route():
	error_message = []
	message = []
	if 'username' not in session:
		return redirect(url_for('index.login_route') + '?url=' + url_for('user.user_edit_route'))
	username = session['username']
	this_user = extensions.get_user(username)
	return render_template('user_edit.html', error_mess = error_message, user = extensions.get_user(username))
