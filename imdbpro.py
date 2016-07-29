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

with open('IMDBPRO.txt') as f:
	content = f.readlines()

rows = []
for row in content:
	print (row.split('\t'))
	rows.append(row)

def insertSQL(row):
	try:
		connection = pymysql.connect(host = 'localhost', user = 'root', password = 'pass', db = 'entertainment_analytics', charset = 'utf8mb4', 
			cursorclass = pymysql.cursors.DictCursor)

		column=row.split("\t")	
		name = column[0]
		link = column[1].strip('\n')

		with connection.cursor() as cursor:

			sql = "INSERT INTO `distributors` (`name`, `link`) VALUES (%s, %s)" 
			cursor.execute(sql, (name, link))
			connection.commit()

			print (name + ' ' + link)

		connection.close()
	except Exception as e:
		print(str(e))


POOL.map(insertSQL, rows)

