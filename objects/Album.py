class Album:
	__id = None
	__username = None
	__title = None
	__created = None
	__lastupdated = None
	__picList = None
	__private = None
	__permissions = None
	__removed_users = None
	__added_users = None
	__updated_privacy = None

	def __init__(self, id, username, title, created, last, private):
		self.__id = id
		self.__username = username
		self.__title = title
		self.__created = created
		self.__lastupdated = last
		self.__private = private
		self.__picList = []
		self.__permissions = {} 
		self.__removed_users = []
		self.__added_users = []
		self.__updated_privacy = False

	def add_pic_to_list(self, pic):
		self.__picList.append(pic)

	def get_id(self):
		return self.__id

	def get_username(self):
		return self.__username

	def get_title(self):
		return self.__title

	def get_permissions(self):
		return self.__permissions

	def get_created(self):
		return self.__created

	def get_lastUpdated(self):
		return self.__lastupdated

	def get_picList(self):
		return self.__picList

	def is_private(self):
		return self.__private

	def set_perm_list(self, inlist):
		print inlist
		self.__permissions = inlist
		print self.__permissions

	def make_private(self):
		if self.__private:
			return
		self.__private = True
		self.__updated_privacy = True
		self.__permissions = {}

	def make_public(self):
		if not self.__private:
			return
		self.__updated_privacy = True
		self.__private = False

	def add_access(self, inusername):
		self.__permissions[inusername] = True
		self.__added_users.append(inusername)

	def remove_access(self, inusername):
		del self.__permissions[inusername]
		self.__removed_users.append(inusername)

	def has_access(self, inusername):
		print self.__permissions
		if inusername in self.__permissions:
			return True
		elif inusername == self.__username:
			return True
		else:
			return False

	def get_added_users(self):
		return self.__added_users

	def get_removed_users(self):
		return self.__removed_users

	def get_permissions_changed(self):
		return self.__updated_privacy
