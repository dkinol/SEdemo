from flask import *
import extensions

''' This set of controllers affects how the users see and edit
lists of albums, not a view of a specific album'''

albums = Blueprint('albums', __name__, template_folder='templates')

@albums.route('/albums', methods=['GET'])
def albums_route():
	name = request.args.get('username')
	if 'username' not in session:
		if name == '':
			return(redirect(url_for('index.login_route') + '?url=' + url_for('albums.albums_route')))
		else:
			publicAlbums = extensions.get_all_public_albums_individual(name)
			return render_template('album_list_nosession.html', name=name, publicAlbums=publicAlbums)
	username = session['username']
	user = extensions.get_user(username)
	return render_template('album_list.html', user=user)

@albums.route('/albums/edit', methods=['GET', 'POST'])
def albums_edit_route():
	if 'username' not in session:
		return(redirect(url_for('index.login_route') + '?url=' + url_for('albums.albums_edit_route')))
	username = session['username']
	if request.method == 'POST':
		if request.form['op'] == 'delete':
			extensions.delete_album(request.form['albumid'])
		elif request.form['op'] == 'add':
			extensions.create_album(request.form['username'], 
				request.form['title'])

	user = extensions.get_user(username)
	return render_template('album_list_edit.html', user=user)
