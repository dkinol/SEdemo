import hashlib

class Photo:
	__picid = None
	__format = None
	__date = None
	__albumID = None
	__nextID = None
	__prevID = None
	__caption = None
	__username_owner = None
	__is_private = None
	__access_list = None

	def __init__(self, inPicid, inFormat, inDate, album, prev, next, caption, userName, isprivate, accesslist):
		self.__picid = inPicid
		self.__format = inFormat
		self.__date = inDate
		self.__albumID = album
		self.__prevID = prev
		self.__nextID = next
		self.__caption = caption
		self.__username_owner = userName
		self.__is_private = isprivate
		self.__access_list = accesslist

	def has_access(self, inusername):
		
		if inusername in self.__access_list:
			return True
		elif inusername == self.__username_owner:
			return True
		else:
			return False

	def is_private(self):
		return self.__is_private

	def get_picid(self):
		return self.__picid

	def get_format(self):
		return self.__format

	def get_date(self):
		return self.__date
	
	def get_albumID(self):
		return self.__albumID

	def get_nextID(self):
		return self.__nextID

	def get_prevID(self):
		return self.__prevID

	def get_caption(self):
		return self.__caption;

	def get_username_owner(self):
		return self.__username_owner

	def hash(self, fileName, userName, album_title):
		hash = hashlib.md5(userName + album_title + fileName)
		self.__picid = hash.hexdigest()

