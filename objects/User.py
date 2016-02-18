import hashlib
import uuid
import re
from email.utils import parseaddr

class User:
	__username = None
	__firstname = None
	__lastname = None
	__password = None
	__salt = None
	__email = None
	__passhashed = None
	# This is a dictionary, mapping Album ids to Album names
	__albumdict = None

	def __init__(self, inUsername, inFirst, inLast, inPass, inEmail):
		self.__username = inUsername
		self.__firstname = inFirst
		self.__lastname = inLast
		self.__password = inPass
		self.__email = inEmail
		self.__salt = ''
		self.__albumdict = {}

	def add_entry(self, inId, inName):
		self.__albumdict[inId] = inName

	# For unit testing
	def set_salt(self, inSalt):
		#print "Input salt "+ inSalt
		self.__salt = inSalt.encode("utf-8")
		#print "After hex encode: " + self.__salt

	# Call this to set salt
	def create_salt(self):
		self.__salt = uuid.uuid4().hex

	def get_username(self):
		return self.__username

	def get_firstname(self):
		return self.__firstname

	def set_firstname(self, inName):
		self.__firstname = inName

	def get_lastname(self):
		return self.__lastname

	def set_lastname(self, inName):
		self.__lastname = inName

	def get_password(self):
		return self.__password

	def set_password(self, inPass):
		self.__salt = ''
		self.__password = inPass

	def get_email(self):
		return self.__email

	def set_email(self, inEmail):
		self.__email= inEmail

	def get_albumdict(self):
		return self.__albumdict

	def get_salt(self):
		return self.__salt

	# Call this to hash a password, call create_salt() before this function
	def hash_pass(self):
		algorithm = 'sha512'
		m = hashlib.new(algorithm)
		m.update(self.__salt + self.__password.encode('utf-8'))
		self.__password = m.hexdigest()

	def validate(self):
		self.print_user_info()
		message = []
		if len(self.__username) < 3:
			message.append('Usernames must be at least 3 characters long')
		if not re.match('^[A-Za-z0-9_]*$', self.__username):
			message.append('Usernames may only contain letters, digits, and underscores')
		if len(self.__password) < 8:
			message.append('Passwords must be at least 8 characters long')
		if len(self.__username) > 20:
			message.append('Username must be no longer than 20 characters')
		if len(self.__firstname) > 20:
			message.append('Firstname must be no longer than 20 characters')
		if len(self.__lastname) > 20:
			message.append('Lastname must be no longer than 20 characters')
		if not re.match('[^@]+@[^@]+\.[^@]+', self.__email):
			message.append('Email address must be valid')
		if len(self.__email) > 20:
			message.append('Email must be no longer than 40 characters')
		if self.__salt == '':
			if not re.match('^[A-Za-z0-9_]*$', self.__password):
				message.append('Passwords may only contain letters, digits, and underscores')
			if not re.match('^(?=.*[a-zA-Z])(?=.*\d).+$', self.__password):
				message.append('Passwords must contain at least one letter and one number')
		return message

	def check_pass(self, password):
		algorithm = 'sha512'
		m = hashlib.new(algorithm)
		m.update(self.__salt + password.encode('utf-8'))
		#print m.hexdigest()
		#print "salt: " + self.__salt
		#print "salt encode: "+ self.__salt.encode('utf-8')
		#print "pass encode: "+ password
		if (m.hexdigest() == self.__password):
			return True
		return False

	def print_user_info(self):
		print "Username: " + self.__username
		print "Firstname: " + self.__firstname
		print "Lastname: " + self.__lastname
		print "Password: " + self.__password
		#print "Salt: " + self.__salt
		print "Email: " + self.__email
		#print "Passhashed: " + self.__passhashed.encode('utf-8')
		#print "Users also have albumdict, not printed here"
