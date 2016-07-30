def scrapeURL(info):
	try:
		companyid = info[0]
		url = info[1] + 'filmography#PAST_FILM'
		soup = browser.get(url).soup

		#print(soup.encode('utf-8'))

		for row in  (soup.find_all(class_="PAST_FILM")[1].find_all('li', class_='')):
			#print (row.encode('utf-8'))

			titleInfo = row.find('span', class_='title-info')
			#print (titleInfo.encode('utf-8'))

			displayTitle = titleInfo.find('span', class_='display-title').a.get_text()
			link = str(titleInfo.find('span', class_='display-title').a)
			link = link[link.index('href="') + 5:link.index('>')].strip('"')
			link = link[:link.index('?ref_=co')]
			print (link)

			imdbid = link.replace('https://pro-labs.imdb.com/title','').strip('/')

			roles = titleInfo.find('span', class_='roles expanding_group').find('span', class_='collapsed').get_text().strip('\n')
			print ("Display title: " + str(displayTitle) + ", Roles: " + str(roles))

			year = row.find('span', class_='year').get_text()
			moviemeter = row.find('span', class_='moviemeter').get_text().strip('\n')
			budget = row.find('span', class_='budget').get_text().strip('\n')
			if not boxoffice:
				boxoffice = 'N/A'
			boxoffice = row.find('span', class_='box-office').get_text().strip('\n')
			if not boxoffice:
				boxoffice = 'N/A'

			print (('Year: %s, Moviemeter: %s, Box Office: %s') % (str(year), str(moviemeter), str(boxoffice)))

			connection = pymysql.connect(host = 'localhost', user = 'root', password = 'pass', db = 'entertainment_analytics', charset = 'utf8mb4', 
				cursorclass = pymysql.cursors.DictCursor)

			with connection.cursor() as cursor:
				sql = (
					"INSERT INTO `filmography` (`imdbid`, `companyid`, `title`, `year`, `roles`, `moviemeter`,`budget`, `boxoffice`) VALUES "
					"(%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE `imdbid`=%s, `title`=%s, `year`=%s, `roles`=%s, `moviemeter`=%s,`budget`=%s, `boxoffice`=%s"
					)

				cursor.execute(sql, (imdbid, companyid, displayTitle, year, roles, moviemeter, budget, boxoffice, imdbid, title, year, roles, moviemeter, budget, boxoffice))

			connection.commit()
			connection.close()
	except Exception as e:
		print (str(e))
#POOL.map(scrapeURL, companies)
