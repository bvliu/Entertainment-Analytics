import pymysql.cursors
from datetime import *
from datetime import datetime
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from functools import partial
import http
import urllib.parse
import urllib.request
import pymysql.cursors
import re

POOL = Pool(cpu_count()*2)

# 10.201.31.179

def storeGenre(info):
	movieID = info[0]
	genres = info[1]
	genreString = [word.lower() for word in genres.replace(',','').split(' ')]
	for index, word in enumerate(genreString):
		genreString[index] = word.replace('-', '_')
		if word == 'sci-fi':
			genreString[index] = 'sci_fi'
		elif word == 'historical':
			genreString[index] = 'history'
		elif word == 'romantic':
			genreString[index] = 'romance'
		elif word == 'period':
			genreString[index] = 'history'
		elif word == 'sports':
			genreString[index] = 'sport'
		elif word == 'concert':
			genreString[index] = 'musical'
		elif word == 'n/a':
			genreString[index] = 'unknown'
		elif word in ['imax', 'epic','short']:
			genreString[index] = 'other'

	print (genreString)

	connection = pymysql.connect(host = 'localhost', user = 'root', password = 'pass', db = 'entertainment_analytics', charset = 'utf8mb4', 
		cursorclass = pymysql.cursors.DictCursor)
	with connection.cursor() as cursor:
		try:
			for column in genreString:
				sql  = 'INSERT INTO `genre` (`id`, `genres`, `' + column + '`) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE `' + column + '`=%s'
				#print (sql)
				cursor.execute(sql, (movieID, genres, '1', '1'))
		except Exception as e:
			print (str(e))
	connection.commit()
	connection.close()

try:
	connection = pymysql.connect(host = 'localhost', user = 'root', password = 'pass', db = 'entertainment_analytics', charset = 'utf8mb4', 
		cursorclass = pymysql.cursors.DictCursor)


	with connection.cursor() as cursor:

		sql = "SELECT `id` FROM `movies`" 
		cursor.execute(sql)

		movies = []
		for movie in cursor:
			movieID = movie['id']
			movies.append(movieID)

		genreTuples = []

		for movie in movies:
			sql = "SELECT `genre` FROM `basics` WHERE `id`=%s"
			cursor.execute(sql, movie)

			for row in cursor:
				genres = row['genre']

			print (movie, genres)
			genreTuples.append((movie, genres))

		POOL.map(storeGenre, genreTuples)



	connection.close()
except Exception as e:
	print(str(e))
