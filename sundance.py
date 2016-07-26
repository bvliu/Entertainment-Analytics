import pymysql.cursors
import csv

# ------------------------------------SUNDANCE SCRAPER---------------------------------------------

def baseScrapingLoop():
	connection = pymysql.connect(host = 'localhost', user = 'root',
		password = 'pass', db = 'entertainment_analytics', charset = 'utf8mb4',
		cursorclass = pymysql.cursors.DictCursor) 

	with open('sundance_master.csv') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for index, row in enumerate(reader):
			print (index, row)
			try:
				year = (row[3].split(' '))[0]
				if (len(year) != 4):
					continue
				else:
					releaseDate = year + '-12-31'
					#print (releaseDate)

				title = row[0]
				filmtype = row[1]
				section = row[2]
				event = row[3]


				with connection.cursor() as cursor:

					exists = False
					findTitleInMovies = "SELECT `id`, `title`, `release_date` FROM `movies` WHERE `title`=%s"
					cursor.execute(findTitleInMovies, title)
					for row in cursor:
						dateResult = str(row['release_date'])[:4]
						if (dateResult == year):
							exists = True
							tempid = row['id']
							sql = (
								"INSERT INTO `misc` (`id`, `film_type`, `section`, `event`) "
								"VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE `film_type`=%s, `section`=%s, `event`=%s"
								)
							cursor.execute(sql, (tempid, filmtype, section, event, filmtype, section, event))

					if not exists:
						sql = (
							"INSERT INTO `movies` (`title`, `release_date`) VALUES (%s, %s) "
							"ON DUPLICATE KEY UPDATE `title`=%s, `release_date`=%s"
							)
						cursor.execute(sql, (title, releaseDate, title, releaseDate))

						sql = "SELECT `id` FROM `movies` WHERE `title`=%s AND release_date=%s"
						cursor.execute(sql, (title, releaseDate))
						for row in cursor:
							print (row)
							primaryid = row['id']

						sql = (
							"INSERT INTO `misc` (`id`, `film_type`, `section`, `event`) "
							"VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE `film_type`=%s, `section`=%s, `event`=%s"
							)
						cursor.execute(sql, (primaryid, filmtype, section, event, filmtype, section, event))


			except Exception as e:
				print (str(e))

	connection.commit()
	connection.close()

if __name__ == '__main__':
	baseScrapingLoop()