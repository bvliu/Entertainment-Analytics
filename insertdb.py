from bs4 import BeautifulSoup
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

with open('allData.txt') as f:
	content = f.readlines()

rows = []
for row in content:
	print (row)
	rows.append(row)

def formatDate(release):
	try:
		release = re.sub("[,]", "", release)
		release = datetime.strptime(release, "%d %b %Y")
		release = release.strftime("%Y-%m-%d")
	except ValueError:
		if release == 'N/A': # If the date format is N/A
			release = None
		elif len(release) == 4: # If the date format is only the year
			release = release + '-01-01'
		elif len(release) > 4: # If the date format is the month then the year (June 1981)
			release = datetime.strptime(release, "%B %Y")
			release = release.strftime("%Y-%m-01")
	#print ("Release Date: " + str(release))
	return release

def formatTime(myTime):
	runtime = int(myTime.replace(' min', ''))

	minutes = runtime%60
	hours = runtime//60

	runtime = str(hours) + ' ' + str(minutes)

	runtime = datetime.strptime(runtime, "%H %M")
	runtime = runtime.strftime("%H:%M:00")
	#print(runtime)	
	return runtime

def insertSQL(row):
	try:
		connection = pymysql.connect(host = 'localhost', user = 'root', password = 'pass', db = 'entertainment_analytics', charset = 'utf8mb4', 
			cursorclass = pymysql.cursors.DictCursor)

		column=row.split("\t")	

		with connection.cursor() as cursor:

			date = formatDate(column[3])

			runtime = column[4]
			if runtime != 'N/A':
				runtime = formatTime(runtime)
			else: 
				runtime = None

			sql = "INSERT INTO `movies` (`title`, `release_date`) VALUES (%s, %s)" 
			cursor.execute(sql, (column[0], date))

			# sql = "SELECT `id` FROM `movies` WHERE `title`=%s AND `release_date`=%s"
			# cursor.execute(sql, (column[0], date))
			# for row in cursor:
			# 	movieID = row['id']

			# sql = "INSERT INTO `basics` (`id`, `title`, `year`, `rating`,`releasedate`, `runtime`, `genre`, `director`, `writer`, `actors`, `plot`, `language`, `country`, `awards`, `metascore`, `imdbrating`, `imdbvote`, `imdbid`, `typeoffilm`, `productioncompany`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
			# cursor.execute(sql, (movieID, column[0],column[1],column[2],date, runtime,column[5],column[6], column[7], column[8],column[9],column[10],column[11],column[12], column[13],column[14],column[15], column[16], column[17], column[18]))

			# sql = "INSERT INTO `misc` (`id`, `imdbid`, `title`, `run_time`,`rating`) VALUES (%s, %s, %s, %s, %s)" 
			# cursor.execute(sql, (movieID, column[16],column[0],runtime,column[2]))
			connection.commit()


			print (column[0])
		connection.close()
	except Exception as e:
		print(str(e))


POOL.map(insertSQL, rows)


#IMDB Basics Files 
#Add to the lists 

# while line: 
# 	column=line.split("\t")

# 	try:
# 		with connection.cursor() as cursor:
# 			sql = "INSERT INTO `basics` (`title`, `year`, `rating`,`releasedate`, `runtime`, `genre`, `director`, `writer`, `actors`, `plot`, `language`, `country`, `awards`, `metascore`, `imdbrating`, `imdbvote`, `imdbid`, `typeoffilm`, `productioncompany`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
# 			cursor.execute(sql, (column[0],column[1],column[2],column[3], column[4],column[5],column[6], column[7], column[8],column[9],column[10],column[11],column[12], column[13],column[14],column[15], column[16], column[17], column[18]))
# 			connection.commit()

# 		#This will deal with the Ratings of the people 
# 		#with connection.cursor() as cursor:
# 		#	sql = "INSERT INTO `ratings` (`imdbid`,`title`, `Rating 10`, `Rating 9`, `Rating 8`, `Rating 7`, `Rating 6`, `Rating 5`, `Rating 4`, `Rating 3`, `Rating 2`, `Rating 1`, `malevotes`, `averagemalevotes`, `femalevotes`, `averagefemalevotes`, `<18`, `average<18`, `male<18`, `averagemale<18`, `female<18`, `averagefemale<18`, `18-29`, `average18-29`, `male18-29`, `averagemale18-29`, `female18-29`, `averagefemale18-29`, `30-44`, `average30-44`,`male30-44`, `averagemale30-44`, `female30-44`, `averagefemale30-44`, `45+`, `average45+`, `male45+`, `averagemale45+`, `female45+`, `averagefemale45+`, `us`, `averageus`, `nonus`, `averagenonus`) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)"
# 		#	cursor.execute(sql, (column[16],column[0], column[48],column[49],column[50],column[51], column[52],column[53],column[54],column[55], column[56], column[57], column[59], column[60], column[62], column[63], column[65], column[66], column[68], column[69], column[71], column[72], column[74], column[75], column[77], column[78], column[80], column[81], column[83], column[84], column[86], column[87], column[89], column[90], column[92], column[93], column[95], column[96], column[98], column[99],                 column[101], column[102], column[104], column[105]))
# 		#	connection.commit()

# 	except Exception as e: 
# 		pass
	
# 	print ("going") 
# 	line=f.readline()


