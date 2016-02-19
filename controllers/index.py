from flask import *
from controllers.support import generate_error_response, send_401, send_403
import extensions
import os

index = Blueprint('index', __name__, template_folder='templates')

@index.route('/')
def main_route():
	publiclist = extensions.get_all_public_albums()
	if 'username' in session:
		uname = session['username']
		privateAlb = extensions.get_user_private_albums(uname)
		otherAccess = extensions.get_private_albums(uname)
		albums = privateAlb + publiclist + otherAccess
	else:
		albums = publiclist
	return render_template("homepage.html", albums=albums)	


@index.route('/api/v1/login', methods=['POST',])
def login_api():
	req = request.get_json(force=True)
	errors = []
	if ('username' not in req) or ('password' not in req):
		errors.push("You did not provide the necessary fields")
		return jsonify(generate_error_response(errors)), 422
	user = extensions.get_user(req['username'])
	if user == None:
		errors.push("Username does not exist")
		return jsonify(generate_error_response(errors)), 404
	user_pass = req['password']
	if user.check_pass(user_pass):
		session['username'] = user.get_username()
		session['firstname'] = user.get_firstname()
		session['lastname'] = user.get_lastname()
		result = {}
		result['username'] = user.get_username()
		return jsonify(result)
	errors.push("Password is incorrect for the specified username")
	return jsonify(generate_error_response(errors)), 422

@index.route('/login', methods=['GET', 'POST'])
def login_route():
	if request.method == 'GET':
		url = request.args.get('url')
		if url == None:
			url = '/'
		#print "geturl: " + url
		return render_template("login.html", error='')

	if request.method == 'POST':
		url = request.args.get('url')
		if url == None:
			url = url_for('index.main_route')
		print request.form['username']
		print request.form['password']
		inuser = extensions.get_user(request.form['username'])
		if inuser == None:
			return render_template("login.html", error='Invalid username')
		user_pass = request.form['password']
		#print "posturl: " + url
		if inuser.check_pass(user_pass):
			session['username'] = inuser.get_username()
			session['firstname'] = inuser.get_firstname()
			session['lastname'] = inuser.get_lastname()
			return redirect(url)
		else:
			return render_template('login.html', error='Invalid password')
	return render_template("login.html")

@index.route('/api/v1/logout', methods=['POST'])
def logout_api():
	if 'username' not in session:
		send_401()
	session.pop('username', None)
	session.pop('firstname', None)
	session.pop('lastname', None)
	return ('', 204)
	

@index.route('/logout', methods=['POST'])
def logout_route():
	print 'got to logout'
	if request.method == 'POST':
		session.pop('username', None)
		session.pop('firstname', None)
		session.pop('lastname', None)
		return redirect(url_for('index.main_route'))
