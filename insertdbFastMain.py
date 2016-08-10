#PURPOSE: This will insert the data from the text files into the database (MariaDB) - table: basics, movies, and misc 

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

#This will open the text file with all of my movie data I scraped from IMDb 
with open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\Redo\\allData.txt') as f:
	content = f.readlines()

#This will go through the rows 
rows = []
for row in content:
	#print (row)
	rows.append(row)

#Formats data with the correct Date in the database YYYY/MM/DD
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

#Formats the time with the correct format (takes out the 'min')
def formatTime(myTime): 
	try: 
		runtime=int(myTime.replace(' min',''))
		#90 min --> 90
		minutes=runtime%60
		#minutes=30 
		hours=runtime//60
		#hours=1

		if minutes<10:
			runtime='0' + str(hours) + ':0' + str(minutes) + ':00'
			runtime=datetime.strptime(runtime, "%H %M")
			runtime=runtime.strftime("%H:%M:00")
		else: 
			runtime='0'+ str(hours)+':' + str(minutes) + ':00'
			runtime=datetime.strptime(runtime, "%H %M")
			runtime=runtime.strftime("%H:%M:00")
		print(runtime)

	except ValueError:
		if runtime=='N/A': 
			runtime=None

	return runtime

#Inserts the data into the database  
def insertSQL(row):
	try:
		connection = pymysql.connect(host = 'localhost', user = 'root', password = 'pass', db = 'entertainment_analytics', charset = 'utf8mb4', 
			cursorclass = pymysql.cursors.DictCursor)

		column=row.split("\t")	

		with connection.cursor() as cursor:

			#Takes the data from each column in the text file. 
			date = formatDate(column[3])

			runtime = column[4]
			if runtime != 'N/A':
				runtime = formatTime(runtime)
			else: 
				runtime = None

			#This will insert into the movies table 
			sql = "INSERT INTO `movies` (`title`, `release_date`) VALUES (%s, %s)" 
			cursor.execute(sql, (column[0], date))

			sql = "SELECT `id` FROM `movies` WHERE `title`=%s AND `release_date`=%s"
			cursor.execute(sql, (column[0], date))
			for row in cursor:
				movieID = row['id']

			#This will insert into the basics table 
			sql = "INSERT INTO `basics` (`title`, `year`, `rating`,`releasedate`, `runtime`, `genre`, `director`, `writer`, `actors`, `plot`, `language`, `country`, `awards`, `metascore`, `imdbrating`, `imdbvote`, `imdbid`, `typeoffilm`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
			cursor.execute(sql, (column[0],column[1],column[2],date, runtime,column[5],column[6], column[7], column[8],column[9],column[10],column[11],column[12], column[13],column[14],column[15], column[16], column[17]))
				
			#This will insert into the misc table 
			sql = "INSERT INTO `misc` (`id`, `imdbid`, `title`, `run_time`,`rating`) VALUES (%s, %s, %s, %s, %s)" 
			cursor.execute(sql, (movieID, column[16],column[0],runtime,column[2]))
			
			connection.commit()

			print (column[0])
		
		connection.close()
	
	except Exception as e:
		print(str(e))


POOL.map(insertSQL, rows)

