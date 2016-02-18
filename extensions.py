from flask.ext.mysqldb import MySQL
from objects.User import User
from objects.Album import Album
from objects.Photo import Photo
from email.utils import parseaddr
import hashlib
import os
import re
from flask import *

mysql = MySQL()

#Gets all Album Ids associated with a user
#Returns them as a list
def get_all_usernames():
	cur = mysql.connection.cursor()
	selector = "SELECT username, firstname, lastname FROM User"
	cur.execute(selector)
	results = []
	for row in cur.fetchall():
		ele = [row['username'], row['firstname'], row['lastname']]
		results.append(ele)
	return results

def get_all_public_albums():
	cur = mysql.connection.cursor()
	selector = "SELECT albumid, title FROM Album WHERE access=%(acc)s"
	cur.execute(selector, {'acc': 'public'})
	results = []
	for row in cur.fetchall():
		ele = [row['albumid'], row['title']]
		results.append(ele)
	return results

def get_user_private_albums(username):
	cur = mysql.connection.cursor()
	selector = "SELECT albumid, title FROM Album WHERE access=%(acc)s AND username=%(uname)s"
	cur.execute(selector, {'acc': 'private','uname':username})
	results = []
	for row in cur.fetchall():
		ele = [row['albumid'], row['title']]
		results.append(ele)
	return results

def get_private_albums(username):
	cur = mysql.connection.cursor()
	selector = "SELECT Album.albumid, Album.title FROM AlbumAccess INNER JOIN Album ON AlbumAccess.albumid=Album.albumid WHERE AlbumAccess.username=%(acc)s"
	cur.execute(selector, {'acc': username})
	results = []
	for row in cur.fetchall():
		ele = [row['albumid'], row['title']]
		results.append(ele)
	return results

def get_album(album_id):
	cur = mysql.connection.cursor()
	selector = "SELECT * FROM Album WHERE albumid=%(album)s"
	cur.execute(selector, {'album': album_id})
	if cur.rowcount == 0:
		abort(404)
	row = cur.fetchone()
	private = True
	if row['access'] == 'public':
		private = False
	result = Album(row['albumid'], row['username'], row['title'], row['created'], row['lastupdated'], private) 

	access_list = {}
	selector = "SELECT username FROM AlbumAccess WHERE albumid=%(id)s"
	cur.execute(selector, {'id' : album_id})
	rows = cur.fetchall()
	for row in rows:
		access_list[row['username']] = True
	result.set_perm_list(access_list)

	selector = "SELECT Photo.picid, Photo.format FROM Photo JOIN Contain ON Contain.picid = Photo.picid WHERE Contain.albumid = %(album)s ORDER BY Contain.sequencenum ASC"
	cur.execute(selector, {'album': album_id })
	rows = cur.fetchall()
	for row in rows: 
		result.add_pic_to_list(get_photo(row['picid']))

	return result

def get_user(username):
	cur = mysql.connection.cursor()
	selector = "SELECT * FROM User WHERE username=%(usr)s"
	cur.execute(selector, {'usr': username})
	if cur.rowcount == 0:
		return None
	row = cur.fetchone()
	split_pass = row['password'].split("$")
	result = User(row['username'], row['firstname'], row['lastname'], split_pass[2], row['email'])
	result.set_salt(split_pass[1])
	selector = "SELECT albumid, title  FROM Album WHERE username=%(usr)s"
	cur.execute(selector, {'usr': username})
	rows = cur.fetchall()
	for row in rows:
		result.add_entry(row['albumid'], row['title'])
	return result

def add_user(inUser):
	cur = mysql.connection.cursor()
	selector = "INSERT INTO User (username, firstname, lastname, password, email) VALUES (%(usr)s, %(first)s, %(last)s, %(pass)s, %(email)s)"
	cur.execute(selector, { 'usr' : inUser.get_username(),
				'first' : inUser.get_firstname(),
				'last' : inUser.get_lastname(),
				'pass' : 'sha512$' + inUser.get_salt() + '$' + inUser.get_password(),
				'email' : inUser.get_email() })
	mysql.connection.commit()

def get_photo(photoId):
	#photo = Photo('space_EagleNebula.jpg', 'jpg',1,1,'football_s4.jpg','space_GalaxyCollision.jpg')
	cur = mysql.connection.cursor()
	selector = "SELECT * FROM Photo WHERE picid =%(pcid)s"
	cur.execute(selector, {'pcid':photoId})
	if cur.rowcount == 0:
		abort(404)
	row = cur.fetchone()
	pid = row['picid']
	form = row['format']
	dat = row['date']

	selector = "SELECT albumid, sequencenum, caption FROM Contain WHERE picid = %(picid)s"
	cur.execute(selector,{'picid':photoId})
	row = cur.fetchone()
	albumnum = row['albumid']
	thisSeqnum = row['sequencenum']
	cap = row['caption']

	selector = "SELECT picid FROM Contain WHERE albumid = %(alid)s AND sequencenum > %(seqnum)s ORDER BY sequencenum ASC"
	cur.execute(selector, {'alid': albumnum, 'seqnum':thisSeqnum})
	if cur.rowcount == 0:
		next = None
	else:
		row = cur.fetchone()
		next = row['picid']

	selector = "SELECT picid FROM Contain WHERE albumid = %(alid)s AND sequencenum < %(seqnum)s ORDER BY sequencenum DESC"
	cur.execute(selector, {'alid': albumnum, 'seqnum':thisSeqnum})
	if cur.rowcount == 0:
		prev = None
	else:
		row = cur.fetchone()
		prev = row['picid']

	selector = "SELECT username, access FROM Album WHERE albumid = %(alid)s"
	cur.execute(selector, {'alid': albumnum})
	row = cur.fetchone()
	username = row['username']
	access = row['access']
	isPrivate = (access == 'private')
	accessList = {}
	if (isPrivate):
		selector = "SELECT username FROM AlbumAccess WHERE albumid = %(alid)s"
		cur.execute(selector, {'alid': albumnum})
		rows = cur.fetchall()
		for row in rows:
			userAccess = row['username']
			accessList[userAccess] = True

	photo = Photo(pid,form,dat,albumnum,prev,next,cap, username, isPrivate, accessList)

	return photo

def update_album(album):
	cur = mysql.connection.cursor()
	added = album.get_added_users()
	for username in added:
		selector = "INSERT INTO AlbumAccess (albumid, username) VALUES (%(id)s, %(user)s)"
		cur.execute(selector, {'id' : album.get_id(), 'user' : username})
		
	removed = album.get_removed_users()
	for username in removed:
		selector = "DELETE FROM AlbumAccess WHERE username=%(user)s"
		cur.execute(selector, {'user' : username})

	permissions_changed = album.get_permissions_changed()
	if permissions_changed and album.is_private():
		selector = "DELETE FROM AlbumAccess WHERE albumid=%(id)s"
		cur.execute(selector, {'id' : album.get_id()})
		selector = "UPDATE Album SET access=%(val)s WHERE albumid=%(id)s"
		cur.execute(selector, {'val' : 'private', 'id' : album.get_id()})
	if permissions_changed and not album.is_private():
		selector = "UPDATE Album SET access=%(val)s WHERE albumid=%(id)s"
		cur.execute(selector, {'val' : 'public', 'id' : album.get_id()})
	mysql.connection.commit()

def delete_album(album_id):
	# Obtains a list of photos
	cur = mysql.connection.cursor()
	selector = "SELECT picid FROM Contain WHERE albumid=%(alb)s"
	cur.execute(selector, {'alb': album_id})
	photo_list = []
	for row in cur.fetchall():
		photo_list.append(row['picid'])
	
	# Deletes Albums and Contain, since Contain has Cascade effect
	selector = "DELETE FROM Album WHERE albumid=%(id)s"
	cur.execute(selector, {'id': album_id})

	# Deletes the Photos
	for pic in photo_list:
		selector = "DELETE FROM Photo WHERE picid=%(id)s"
		cur.execute(selector, {'id': pic})

	# Deletes the album from AlbumAccess
	selector = "DELETE FROM AlbumAccess WHERE albumid=%(id)s"
	cur.execute(selector, { 'id': album_id })

	# Commit changes so data is perminently deleted
	mysql.connection.commit()

def create_album(in_username, in_title):
	cur = mysql.connection.cursor()
	selector = "INSERT INTO Album (title, created, lastupdated, username, access) VALUES (%(title)s, CURDATE(), CURDATE(), %(username)s, 'private')"
	cur.execute(selector, {'title': in_title, 'username': in_username})
	mysql.connection.commit()

def add_photo(file, album, cap):
	cur = mysql.connection.cursor()
	photoInfo = file.filename.split('.')
	thisAlbum = get_album(album)
	hashId = hashlib.md5(thisAlbum.get_username() + thisAlbum.get_title() + file.filename)
	if (photoInfo[1] =='jpg' or photoInfo[1] =='png' or photoInfo[1] =='bmp' or photoInfo[1] =='gif'):
		selector = "SELECT picid FROM Contain WHERE picid=%(id)s"
		cur.execute(selector, { 'id' : hashId.hexdigest() })
		if cur.rowcount != 0:
			return
		# Saves file to filesystem
		file.save('static/images/' + hashId.hexdigest() + '.' + photoInfo[1])
		selector = "INSERT INTO Photo (picid, format, date) VALUES (%(picid)s, %(format)s, CURDATE())"
		cur.execute(selector, {'picid': hashId.hexdigest(), 'format': photoInfo[1]})
		mysql.connection.commit()
		thisSeqnum = 0
		selector = "SELECT sequencenum FROM Contain WHERE albumid=%(alid)s"
		cur.execute(selector, {'alid':album})
		if cur.rowcount == 0:
			thisSeqnum = 0
		else:
			rows = cur.fetchall()
			for row in rows:
				if row['sequencenum'] > thisSeqnum:
					thisSeqnum = row['sequencenum']
			thisSeqnum = thisSeqnum + 1
		selector = "INSERT INTO Contain (albumid, picid, caption, sequencenum) VALUES (%(alid)s, %(pcid)s, %(cap)s, %(seq)s)"
		cur.execute(selector, {'alid': album, 'pcid': hashId.hexdigest(), 'cap': cap, 'seq': thisSeqnum})
		mysql.connection.commit()
	else:
		print 'not valid photo type'

def delete_photo(file, album):
	cur = mysql.connection.cursor()
	#os.remove('static/images/' + file)
	selector = "SELECT format FROM Photo WHERE picid=%(pic)s"
	cur.execute(selector, { 'pic': file })
	if cur.rowcount == 0:
		return False
	row = cur.fetchone()
	os.remove('static/images/' + file + '.' + row['format'])
	photoInfo = file.split('.')
	selector = "DELETE FROM Contain WHERE picid=%(pic)s"
	cur.execute(selector, {'pic': photoInfo[0]})
	mysql.connection.commit()
	selector = "DELETE FROM Photo WHERE picid=%(pic)s"
	cur.execute(selector, {'pic': photoInfo[0]})
	mysql.connection.commit()
	return True

def update_user(inuser):
	cur = mysql.connection.cursor()
	selector = "UPDATE User SET firstname=%(first)s, lastname=%(last)s, email=%(newEmail)s, password=%(pass)s WHERE username=%(username)s"
	temp = {'first': inuser.get_firstname(), 
			'last': inuser.get_lastname(), 
			'newEmail': inuser.get_email(), 
			'pass': 'sha512$' + inuser.get_salt() + '$' + inuser.get_password(),
			'username': inuser.get_username()}
	cur.execute(selector, temp)
	mysql.connection.commit()

def update_photo_caption(pic_id, new_cap):
	cur = mysql.connection.cursor()
	selector = "UPDATE Contain SET caption=%(cap)s WHERE picid=%(id)s"
	cur.execute(selector, {'cap': new_cap, 'id': pic_id})
	selector = "UPDATE Album INNER JOIN Contain ON Contain.albumid=Album.albumid SET Album.lastupdated=CURDATE() WHERE Contain.picid=%(id)s;"
	cur.execute(selector, {'id': pic_id})
	mysql.connection.commit()

def get_all_public_albums_individual(name):
	cur = mysql.connection.cursor()
	selector = "SELECT albumid, title FROM Album WHERE access=%(acc)s AND username=%(nm)s"
	cur.execute(selector, {'acc': 'public', 'nm':name})
	results = []
	for row in cur.fetchall():
		ele = [row['albumid'], row['title']]
		results.append(ele)
	return results

