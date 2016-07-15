import pymysql.cursors
import csv

# ------------------------------------SUNDANCE SCRAPER---------------------------------------------

connection = pymysql.connect(host = 'localhost', user = 'root',
	password = 'pass', db = 'entertainment_analytics', charset = 'utf8mb4',
	cursorclass = pymysql.cursors.DictCursor) 

data = csv.reader(file('sundance_master.csv'))
print (data)

