#PURPOSE: This will insert the ratings into the database (MariaDB)-  table: ratings 

import pymysql.cursors
from datetime import *
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from functools import partial
import http
import urllib.parse
import urllib.request
import re

POOL = Pool(cpu_count()*2)

#This will open the text file with my total list of data 
with open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\Redo\\ProAndRating\\totalList.txt') as f: 
	content=f.readlines()
rows=[]

for row in content: 
	rows.append(row)

def insertSQL(row): 
	try:
		# Connect to the database with pass and other info 
		connection = pymysql.connect(host = 'localhost', user = 'root', password = 'pass', db = 'entertainment_analytics', charset = 'utf8mb4', 
			cursorclass = pymysql.cursors.DictCursor)

		column=row.split("\t")

		with connection.cursor() as cursor:

			sql= "SELECT `id` FROM `basics` WHERE `Title`=%s"

			#CHANGE
			cursor.execute(sql, (column[0]))
			
			for row in cursor:
				print(row)
				ID=row['id']
				#Title=row['Title']

			sql = "INSERT INTO `ratings`  (`id`,`Title`, `ProductionCo`, `Rating 10`, `Rating 9`, `Rating 8`, `Rating 7`, `Rating 6`, `Rating 5`, `Rating 4`, `Rating 3`, `Rating 2`, `Rating 1`,`MaleVotes`, `AverageMaleVotes`, `FemaleVotes`, `AverageFemaleVotes`, `<18`, `Average<18`, `Male<18`, `AverageMale<18`, `Female<18`, `AverageFemale<18`, `18-29`, `Average18-29`, `Male18-29`, `AverageMale18-29`, `Female18-29`, `AverageFemale18-29`, `30-44`, `Average30-44`, `Male30-44`, `AverageMale30-44`, `Female30-44`, `AverageFemale30-44`, `45+`, `Average45+`, `Male45+`, `AverageMale45+`, `Female45+`, `AverageFemale45+`, `US`, `AverageUS`, `NonUS`, `AverageNonUS`, `column[0]`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)" 

			#This will collect the columns with the data 
			cursor.execute(sql, (ID, column[0], column[2], column[4], column[5],column[6],column[7],column[8],column[9],column[10], column[11],column[12], column[13], column[14],column[15], column[16], column[17], column[18],column[19],column[20],column[21],column[22],column[23], column[24],column[25], column[26],column[27], column[28], column[29], column[30],column[31],column[32],column[33],column[34],column[35], column[36],column[37], column[38],column[39], column[40], column[41], column[42],column[43],column[44],column[45]))
			connection.commit()

	except Exception as e: 
		print (str(e))
		
POOL.map(insertSQL,rows)
	
connection.close()