import pymysql.cursors
from datetime import *


def formatDate(release):
	try:
		release = datetime.strptime(release, "%d %b %Y")
		release = release.strftime("%Y-%m-%d")
	except ValueError:
		if release == 'N/A': # If the date format is N/A
			release = None
	return release

if __name__ == "__main__":	


	# Connect to the database
	connection = pymysql.connect(host = 'localhost', user = 'root', password = 'pass', db = 'imdb', charset = 'utf8mb4', 
		cursorclass = pymysql.cursors.DictCursor)

	f = open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\Redo\\allDataPart2.txt','r')

	line=f.readline()

	#IMDB Basics Files 
	#Add to the lists 

	while line: 
		column=line.split("\t")

		try:
			with connection.cursor() as cursor:

				sql= "SELECT `id` FROM `basics` WHERE `Title`=%s AND releasedate=%s"

				cursor.execute(sql, (column[0], column[3]))
				
				for row in cursor:
					ID=row['id']

				sql = "INSERT INTO `movieList`  (`id`,`Release_Date`, `Title`) VALUES (%s, %s, %s)" 
				print (formatDate(column[3]), column[0])
				cursor.execute(sql, (ID, formatDate(column[3]),column[0]))

			connection.commit()

		except Exception as e: 
			print (str(e))
		
		#print ("going") 
		line=f.readline()


	connection.close()