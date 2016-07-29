"""Example app to login to imdbPRO"""
import argparse
import mechanicalsoup
import pymysql
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from bs4 import BeautifulSoup

POOL = Pool(cpu_count()*2)

login_url = 'https://pro-labs.imdb.com/login'

USERNAME = 'liu.b97@gmail.com'
#USERNAME = 'liu_brandon@bah.com'
PASSWORD = 'brandon229271'

browser = mechanicalsoup.Browser()


login_page = browser.get(login_url)
soup = login_page.soup

login_form = soup.select("#content_box")[0].select("form")[0]

# specify username and password
login_form.select("#email")[0]['value'] = USERNAME
login_form.select("#password")[0]['value'] = PASSWORD

page2 = browser.submit(login_form, login_page.url)

connection = pymysql.connect(host = 'localhost', user = 'root', password = 'pass', db = 'entertainment_analytics', charset = 'utf8mb4', 
	cursorclass = pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
	companies = []
	sql = 'SELECT `companyid`, `link` FROM `distributors`'
	cursor.execute(sql)
	for company in cursor:
		companyid = company['companyid']
		link = company['link']
		companies.append((companyid, link))

connection.commit()
connection.close()


def scrapeURL(info):
	companyid = info[0]
	url = info[1] + 'filmography#PAST_FILM'
	soup = browser.get(url).soup

	print(soup.encode('utf-8'))

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

#POOL.map(scrapeURL, companies)

for company in companies:
	print (company[1])
	scrapeURL(company)