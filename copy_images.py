import glob 
import string
import shutil
from objects.Photo import Photo

sports = [f for f in glob.glob('static/images/safe/sports*.jpg')]
football = [f for f in glob.glob('static/images/safe/football*.jpg')]
worlds = [f for f in glob.glob('static/images/safe/world*.jpg')]
space = [f for f in glob.glob('static/images/safe/space*.jpg')]

allpics = [[sports, 'sportslover', 'I love sports'], 
	[football, 'sportslover', 'I love football'] , 
	[worlds, 'traveler', 'Around The World'],
	[space, 'spacejunkie', 'Cool Space Shots']]

for i in range(len(allpics)):
	for num in range(len(allpics[i][0])):
		pic = string.replace(allpics[i][0][num], 'static/images/safe/', '')
		photo = Photo(pic, '.jpg', None, i, None, None, None)
		photo.hash(pic, allpics[i][1], allpics[i][2])
		shutil.copyfile('static/images/safe/' + pic, 'static/images/' + photo.get_picid() + '.jpg')
