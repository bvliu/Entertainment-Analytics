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
connection = pymysql.connect(host = 'localhost', user = 'root', password = 'pass', db = 'entertainment_analytics', charset = 'utf8mb4', 
	cursorclass = pymysql.cursors.DictCursor)
4
with connection.cursor() as cursor:
	sql = "SELECT `id`, `country` FROM `basics`"

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
