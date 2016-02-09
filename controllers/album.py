from flask import * 
import extensions
from werkzeug import secure_filename
from objects.Photo import Photo
from objects.Album import Album
import os

album = Blueprint('album', __name__, template_folder='templates')

@album.route('/album', methods=['GET'])
def album_route():
	albumname = request.args.get('id')
	album = extensions.get_album(albumname)
	if album.is_private():
		if 'username' not in session:
			return redirect(url_for('index.login_route') + '?url=' + url_for('album.album_route') + '?id=' + albumname)
		elif album.has_access(session['username']):
			return render_template('album.html', album = album)
		else:
			abort(403)
	try: 
		return render_template('album.html', album = album)
	except TemplateNotFound:
		abort(404)

@album.route('/pic', methods=['GET', 'POST'])
def pic_route():
	pic = request.args.get('id')
	photo = extensions.get_photo(pic)
	if request.method == 'POST':
		if 'username' in session:
			if photo.get_username_owner() == session['username']:
				if request.form['op'] == 'caption':
					extensions.update_photo_caption(request.form['picid'], request.form['caption'])
					photo = extensions.get_photo(pic)
					return render_template('full_pic.html', photo = photo, edit = True)
		abort(403)
					
	if photo.is_private():
		if 'username' not in session: 
			return redirect(url_for('index.login_route') + '?url=' + url_for('album.pic_route') + '?id=' + pic)
		elif photo.has_access(session['username']):
			edit = (photo.get_username_owner() == session['username'])
			print 'Edit: ' + edit
			return render_template('full_pic.html', photo = photo, edit = edit)
		else:
			abort(403)

	if 'username' in session:
		if photo.get_username_owner() == session['username']:
			return render_template('full_pic.html', photo = photo, edit = True)

	return render_template('full_pic.html', photo = photo, edit = False)

@album.route('/album/edit', methods=['GET', 'POST'])
def album_edit_route():
	albumname = request.args.get('id')
	if 'username' not in session:
		return redirect(url_for('index.login_route') + '?url=' + url_for('album.album_edit_route') + '?id=' + albumname)
	album = extensions.get_album(albumname)
	if album.get_username() != session['username']:
		abort(403)
	if request.method == 'POST':
		if request.form['op'] == 'add':
			if request.files['file'] != None:
				file = request.files['file']
				extensions.add_photo(file, albumname, '') 
		if request.form['op'] == 'delete':
			if request.form['file'] == None or request.form['albumid'] == None:
				abort(404)
			result = extensions.delete_photo(request.form['file'], albumname)
			if result == False:
				abort(404)
		if request.form['op'] == 'access':
			album = extensions.get_album(albumname)
			if request.form['access'] == 'private':
				album.make_private()
				extensions.update_album(album)
			if request.form['access'] == 'public':
				album.make_public()
				extensions.update_album(album)
		if request.form['op'] == 'grant':
			album = extensions.get_album(albumname)
			if album.is_private():
				if not album.has_access(request.form['username']):
					album.add_access(request.form['username'])
					extensions.update_album(album)
		if request.form['op'] == 'revoke':
			album = extensions.get_album(albumname)
			if album.is_private():
				album.remove_access(request.form['username'])
				extensions.update_album(album)

	albumname = request.args.get('id')
	album = extensions.get_album(albumname)
	return render_template('album_edit.html', album = album, permissions=album.get_permissions())

