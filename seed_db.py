from objects.Photo import Photo

sql = open('sql/load_data.sql', 'w')

users = ['sportslover', 'traveler', 'spacejunkie']

#Create Users
sql.write('INSERT INTO User\n')
sql.write('VALUES ("sportslover", "Paul", "Walker", "sha512$8ec61415f1eb4afba45fa95e164a73e5$a8156f5e122a936e55512ccad145e72581c20853d8ceee8fc4ab535bead173dfb6625dd1d0eaccc9ace73008c135ef5eecb0b452470d007fde088602659ad9a2", "sportslover@hotmail.com");\n')
sql.write('INSERT INTO User\n')
sql.write('VALUES ("traveler", "Rebecca", "Travolta", "sha512$1c662feb81e84cd78cf8d6a96e912ebb$eed150f49e6669c4aee79b0f1ed238ec557e8a6dc1af8c8b4dd393a1a6f0926b97bb537fc7a7af95db36982eaa90a313d4968cdc03112321e9dbb3c4aba65337", "rebt@explorer.org");\n')
sql.write('INSERT INTO User\n')
sql.write('VALUES ("spacejunkie", "Bob", "Spacey", "sha512$523bbfca143d4676b5ecfc8ee42aca6d$fae41640d635cb42c3631e5a66a997e6f6ebfd25f6bb3f9777107d848c24bd2db9767242e803a881dbc5af73ddbf7ee80d1d855db2568061bfb2ca21fcf2dd5f", "bspace@spacejunkies.net");\n')

# Create Albums
name_to_album = [['sportslover', 'I love sports'], ['sportslover', 'I love football'],
	['traveler', 'Around The World'],
	['spacejunkie', 'Cool Space Shots']]
for entry in name_to_album:
	sql.write('INSERT INTO Album (title, created, lastupdated, username, access)\n')
	if entry[1] == 'I love sports' or entry[1] == 'Around The World':
		sql.write('VALUES ("' + entry[1] + '", \"2016-01-01\", \"2016-01-01\", "' + entry[0] + '", \"public\");\n')
	else:
		sql.write('VALUES ("' + entry[1] + '", \"2016-01-01\", \"2016-01-01\", "' + entry[0] + '", \"private\");\n')

# Create Pictures
import glob
import string
sports = [f for f in glob.glob('static/images/safe/sports*.jpg')]
football = [f for f in glob.glob('static/images/safe/football*.jpg')]
worlds = [f for f in glob.glob('static/images/safe/world*.jpg')]
space = [f for f in glob.glob('static/images/safe/space*.jpg')]

sports = sorted(sports, key=lambda s: s.lower())
football = sorted(football, key=lambda s: s.lower()) 
worlds = sorted(worlds, key=lambda s: s.lower())
space = sorted(space, key=lambda s: s.lower()) 

allpics = [[sports, 'sportslover', 'I love sports'], 
	[football, 'sportslover', 'I love football'] , 
	[worlds, 'traveler', 'Around The World'],
	[space, 'spacejunkie', 'Cool Space Shots']]

for i in range(len(allpics)):
	for num in range(len(allpics[i][0])):
		pic = string.replace(allpics[i][0][num], 'static/images/safe/', '')
		photo = Photo(pic, '.jpg', None, i, None, None, None, None, None, None)
		photo.hash(pic, allpics[i][1], allpics[i][2])
		sql.write('INSERT INTO Photo\n')
		sql.write('VALUES (\"' + photo.get_picid() + '\", \"jpg\", \"2016-01-01\");\n')
		sql.write('INSERT INTO Contain\n')
		sql.write('VALUES ('+ str(i + 1) + ', \"' + photo.get_picid() + '\", \"\", ' + str(num) + ');\n')
#sql.write('INSERT INTO Photo\n')

