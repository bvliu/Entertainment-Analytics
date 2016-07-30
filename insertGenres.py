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

# if __name__ == "__main__":	

# 	# Connect to the database
# 	connection = pymysql.connect(host = 'localhost', user = 'root', password = 'pass', db = 'imdb', charset = 'utf8mb4', 
# 		cursorclass = pymysql.cursors.DictCursor)

# 	#f = open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\Redo\\finishedPart2.txt','r')

# 	#line=f.readline()

# 	#IMDB Basics Files 
# 	#Add to the lists 

# 	#while line: 
# 		#column=line.split("\t")

# 	try:
# 		with connection.cursor() as cursor:

# 			sql= "SELECT `id`, 'genre', 'Title' FROM `basics`"
# 			cursor.execute(sql)
			
# 			for row in cursor:
# 				ID=row['id']
# 				Genres=row['genre']
# 				Title=row['Title']

# 				isForeign=0
# 				isUnknown=0
# 				isOther=1

# 				if "N\A" in Genres: 
# 					isUnknown=1
# 					isOther=0

# 				#Genres and the 1/0
# 				isAction=0 
# 				if "Action" in Genres: 
# 					isAction=1
# 					isOther=0

# 				print(isAction)
			
# 				isBiography=0 
# 				if "Biography" in Genres:
# 					isBiography=1 
# 					isOther=0

# 				print(isBiography)

# 				isDocumentary=0 
# 				if "Documentary" in Genres: 
# 					isDocumentary=1
# 					isOther=0

# 				print(isDocumentary)

# 				isFantasy=0 
# 				if "Fantasy" in Genres: 
# 					isFantasy=1
# 					isOther=0

# 				print(isFantasy)

# 				isHistory=0 
# 				if "History" in Genres: 
# 					isHistory=1
# 					isOther=0

# 				print(isHistory)

# 				isMusical=0 
# 				if "Musical" in Genres: 
# 					isMusical=1
# 					isOther=0

# 				print(isMusical)

# 				isReality=0
# 				if "Reality-TV" in Genres: 
# 					isReality=1
# 					isOther=0

# 				print(isReality)

# 				isSport=0
# 				if "Sport" in Genres: 
# 					isSport=1
# 					isOther=0

# 				print(isSport)

# 				isWar=0
# 				if "War" in Genres: 
# 					isWar=1
# 					isOther=0

# 				print(isWar)

# 				isAdventure=0 
# 				if "Adventure" in Genres: 
# 					isAdventure=1
# 					isOther=0

# 				print(isAdventure)

# 				isComedy=0
# 				if "Comedy" in Genres: 
# 					isComedy=1

# 				print(isComedy)

# 				isDrama=0 
# 				if "Drama" in Genres: 
# 					isDrama=1
# 					isOther=0

# 				print(isDrama)

# 				isFilmNoir=0
# 				if "Film-Noir" in Genres: 
# 					isFilmNoir=1
# 					isOther=0

# 				print(isFilmNoir)

# 				isHorror=0 
# 				if "Horror" in Genres: 
# 					isHorror=1
# 					isOther=0

# 				print(isHorror)

# 				isMystery=0 
# 				if "Mystery" in Genres: 
# 					isMystery=1
# 					isOther=0

# 				print(isMystery)

# 				isRomance=0 
# 				if "Romance" in Genres: 
# 					isRomance=1
# 					isOther=0

# 				print(isRomance)

# 				isTalk=0
# 				if "Talk-Show" in Genres: 
# 					isTalk=1
# 					isOther=0

# 				print(isTalk)

# 				isWestern=0 
# 				if "Western" in Genres: 
# 					isWestern=1
# 					isOther=0

# 				print(isWestern)

# 				isAnimation=0 
# 				if "Animation" in Genres: 
# 					isAnimation=1
# 					isOther=0

# 				print(isAnimation)
				
# 				isCrime=0 
# 				if "Crime" in Genres: 
# 					isCrime=1
# 					isOther=0

# 				print(isCrime)

# 				isFamily=0 
# 				if "Family" in Genres: 
# 					isFamily=1
# 					isOther=0

# 				print(isFamily)

# 				isGame=0 
# 				if "Game-Show" in Genres: 
# 					isGame=1
# 					isOther=0

# 				print(isGame)

# 				isMusic=0
# 				if "Music" in Genres: 
# 					isMusic=1
# 					isOther=0

# 				print(isMusic)

# 				isNews=0
# 				if "News" in Genres: 
# 					isNews=1
# 					isOther=0

# 				print(isNews)

# 				isSciFi=0
# 				if "Sci-Fi" in Genres: 
# 					isSciFi=1
# 					isOther=0

# 				print(isSciFi)

# 				isThrill=0  
# 				if "Thriller" in Genres: 
# 					isThrill=1
# 					isOther=0

# 				print(isThrill)
# 				print(isOther)
# 				print(isUnknown)

# 				sql = "INSERT INTO `genre`  (`id`,`Genres`, `Title`, `Foreign`, `Action`, `Biography`, `Documentary`, `Fantasy`, `History`, `Musical`, `Reality_TV`, `Sport`, `War`, `Adventure`, `Comedy`, `Drama`, `Film_Noir`, `Horror`, `Mystery`, `Romance`, `Talk_Show`, `Western`, `Animation`, `Crime`, `Family`, `Game_Show`, `Music`, `News`, `Sci_Fi`, `Thriller`, `Other`, `Unknown`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
# 				cursor.execute(sql, (ID, Genres, Title, isForeign, isAction, isBiography, isDocumentary, isFantasy, isHistory, isMusical, isReality, isSport, isWar, isAdventure, isComedy, isDrama, isFilmNoir, isHorror, isMystery, isRomance, isTalk, isWestern, isAnimation, isCrime, isFamily, isGame, isMusic, isNews, isSciFi, isThrill, isOther, isUnknown))

# 		connection.commit()

# 	except Exception as e: 
# 		print(str(e))
		
# 		#line=f.readline()

# 	connection.close()
