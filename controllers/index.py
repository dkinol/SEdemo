from flask import *
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


@index.route('/logout', methods=['POST'])
def logout_route():
	print 'got to logout'
	if request.method == 'POST':
		session.pop('username', None)
		session.pop('firstname', None)
		session.pop('lastname', None)
		return redirect(url_for('index.main_route'))
