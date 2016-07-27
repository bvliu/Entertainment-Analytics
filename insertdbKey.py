import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host = 'localhost', user = 'root', password = 'pass', db = 'imdb', charset = 'utf8mb4', 
	cursorclass = pymysql.cursors.DictCursor)

f = open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\scrapeIMDbDoc\\Part3FinalTesting.txt','r')

line=f.readline()

while line: 
	column=line.split("\t")

	try: 
		with connection.cursor() as cursor:
			sql = "REPLACE INTO `basics` (`imdbid`, `title`, `plot`, `director`, `writer`,`actors`, `keywords`) VALUES (%s, %s, %s, %s, %s, %s, %s)" 
			cursor.execute(sql, (column[1],column[0],column[2],column[6],column[7], column[8], column[9]))
			connection.commit()

		with connection.cursor() as cursor:
			sql = "REPLACE INTO `genre` (`imdbid`, `title`, `action`,`biography`, `documentary`, `fantasy`, `history`, `musical`, `reality_tv`, `sport`, `war`, `adventure`, `comedy`, `drama`, `film_noir`, `horror`, `mystery`, `romance`, `talk_show`, `western`, `animation`, `crime`, `family`, `game_show`, `music`, `news`, `sci_fi`, `thriller`, `other`, `unknown`) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)"
			cursor.execute(sql, (column[1],column[0],column[12],column[13],column[14], column[15],column[16],column[17], column[18], column[19],column[20],column[21], column[22],column[23],column[24], column[25], column[26],column[27],column[28], column[29],column[30],column[31], column[32], column[33],column[34],column[35], column[36],column[37],column[38], column[39]))
			connection.commit()

	except Exception as e: 
		pass

	print (column[0]) 
	line=f.readline()

connection.close()