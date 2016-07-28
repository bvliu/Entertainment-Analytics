import pymysql.cursors

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
			sql = "INSERT INTO `basics` (`title`, `year`, `rating`,`releasedate`, `runtime`, `genre`, `director`, `writer`, `actors`, `plot`, `language`, `country`, `awards`, `metascore`, `imdbrating`, `imdbvote`, `imdbid`, `typeoffilm`, `productioncompany`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
			cursor.execute(sql, (column[0],column[1],column[2],column[3], column[4],column[5],column[6], column[7], column[8],column[9],column[10],column[11],column[12], column[13],column[14],column[15], column[16], column[17], column[18]))
			connection.commit()

		with connection.cursor() as cursor:
			sql = "INSERT INTO `misc` (`imdbid`, `title`, `run_time`,`rating`) VALUES (%s, %s, %s, %s)" 
			cursor.execute(sql, (column[16],column[0],column[4],column[2]))
			connection.commit()

		#This will deal with the Ratings of the people 
		#with connection.cursor() as cursor:
		#	sql = "INSERT INTO `ratings` (`imdbid`,`title`, `Rating 10`, `Rating 9`, `Rating 8`, `Rating 7`, `Rating 6`, `Rating 5`, `Rating 4`, `Rating 3`, `Rating 2`, `Rating 1`, `malevotes`, `averagemalevotes`, `femalevotes`, `averagefemalevotes`, `<18`, `average<18`, `male<18`, `averagemale<18`, `female<18`, `averagefemale<18`, `18-29`, `average18-29`, `male18-29`, `averagemale18-29`, `female18-29`, `averagefemale18-29`, `30-44`, `average30-44`,`male30-44`, `averagemale30-44`, `female30-44`, `averagefemale30-44`, `45+`, `average45+`, `male45+`, `averagemale45+`, `female45+`, `averagefemale45+`, `us`, `averageus`, `nonus`, `averagenonus`) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s, %s)"
		#	cursor.execute(sql, (column[16],column[0], column[48],column[49],column[50],column[51], column[52],column[53],column[54],column[55], column[56], column[57], column[59], column[60], column[62], column[63], column[65], column[66], column[68], column[69], column[71], column[72], column[74], column[75], column[77], column[78], column[80], column[81], column[83], column[84], column[86], column[87], column[89], column[90], column[92], column[93], column[95], column[96], column[98], column[99],                 column[101], column[102], column[104], column[105]))
		#	connection.commit()

	except Exception as e: 
		pass
	
	print ("going") 
	line=f.readline()


connection.close()