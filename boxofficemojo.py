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

# ------------------------------------BOX OFFICE MOJO SCRAPER---------------------------------------------

BASE_YEAR = "2016"
CURRENT_YEAR = "2016"

# General http address for Box Office Mojo
BOM = "http://www.boxofficemojo.com"

NUM_THREADS = cpu_count() * 2
POOL = Pool(NUM_THREADS)

MASTER_URLS = []

# Keep track of primary keys for the time sensitive table
CURRENT_TITLE = ""

def getURLs():

	years = []

	# Loop through each year starting from the first year (1980) to the current year, set above
	for year in range(int(BASE_YEAR), int(CURRENT_YEAR) + 1):

		# List of the (year) top grossing films, which will be parsed for the URLs
		url = "http://www.boxofficemojo.com/yearly/chart/?page=1&view=releasedate&view2=domestic&yr=1980&p=.htm"
		url = url.replace('yr=1980', 'yr=' + str(year))
		#print (str(year))
		years.append(url)

	POOL.map(scrapeMoviesFromYear, years)

# Iterate through each of the individual pages under the year, 0-100 101-200 etc.
def scrapeMoviesFromYear(url):

	# Keep track of the current page
	currentPage = 0

	# Want to find every movie url for the given year
	while True:
		currentPage += 1
		url = url.replace("?page=" + str(currentPage - 1), "?page=" + str(currentPage))
		#print (url)
		#print ("Page " + str(currentPage))

		# Try to open the html and catch any exceptions doing so
		try:
			with urllib.request.urlopen(url) as response:	
				html = response.read()
		except Exception as e:
			print ("scrapeMoviesFromYear: html request error " + str(type(e)) + str(e))

		# base case, if we've reached the end of the pages then stop the loop
		if "There was an error processing this request" in str(html):
			break
		
		# else we do this:
		soup = BeautifulSoup(html, "html.parser")

		# Search the soup for the <a tag that precedes all href links
		for link in soup.find_all('a'):
			name = str(link.get('href'))

			# if movies is in the link then it's the one we're looking for,
			# not ref = ft is a special case that we don't want to be in the list
			if '/movies/' in name and 'ref=ft' not in name: 
				movieurl = BOM + name
				print(movieurl)
				MASTER_URLS.append(movieurl)

# Iterate through every year
def baseScrapingLoop():

	# Make sure we start off with a blank SQL database CHANGE THIS LATER
	#emptyTable('movie_master')

	#try:

		#func = partial(scrapeDataMovieMaster, connection = connection)
	POOL.map(scrapeDataMovieMaster, MASTER_URLS)
		# for url in MASTER_URLS:
		# 	scrapeDataMovieMaster(url, connection)

	# 	connection.commit()

	# finally:
	# 	connection.close()



def scrapeDataMovieMaster(url):

	connection = pymysql.connect(host = 'localhost', user = 'root',
		password = 'pass', db = 'entertainment_analytics', charset = 'utf8mb4',
		cursorclass = pymysql.cursors.DictCursor) 

	# Try to scrape the data and if there are any errors then skip
	# Errors include http and encoding errors for opening the html
	try:
		with urllib.request.urlopen(url) as response:

			# gets the raw html code from the URL
			html = response.read()
			#print (html)

			# Use Beautiful Soup to organize the html into a more readable way
			soup = BeautifulSoup(html, 'html.parser')
			#print (soup.encode("utf-8"))
			readStaticData(soup.find_all('b'), connection)

	except Exception as e:

		print ("Error scraping movie data " + str(type(e)) + " " + url)
		print (e)
		return

	finally:
		connection.commit()
		connection.close()

def readStaticData(info, connection):

	# Need try-except because sometimes the information is not there
	# 1 = title

	try:
		title = info[1].getText()
	except IndexError:
		print ('IndexError')
		return
	print ("Title: " + title)


	# 2 = domestic total as of some date
	# Comes in this format: $141,319,928, needs to be made an int

	total = info[2].getText().replace(' ', '')
	total = total.replace('(Estimate)', '')
	total = int(re.sub('[$,]', '', total))
	#print ("Domestic Total Gross: " + str(total))

	if "Domestic Lifetime Gross" in info[3].getText():
		del info[3]

	# 3 = distributor

	distributor = info[3].getText()
	#print ("Distributor: " + distributor)

	# 4 = release date
	# Format Release Date: November 12, 2008 needs to be in yyyy-mm-dd

	release = info[4].getText()
	try:
		release = re.sub("[,]", "", release)
		release = datetime.strptime(release, "%B %d %Y")
		release = release.strftime("%Y-%m-%d")
	except ValueError:
		if release == 'N/A': # If the date format is N/A
			release = None
		elif len(release) == 4: # If the date format is only the year
			release = release + '-01-01'
		elif len(release) > 4: # If the date format is the month then the year (June 1981)
			release = datetime.strptime(release, "%B %Y")
			release = release.strftime("%Y-%m-01")
	print ("Release Date: " + str(release))

	# 5 = Genre

	genre = info[5].getText()
	#print ("Genre: " + genre)

	# 6 = Runtime
	# format 2 hrs. 0 min. -> 02:00:00
	runtime = info[6].getText()
	if runtime != 'N/A':
		temp = runtime.split(' ')
		runtime = temp[0] + " " +temp[2]
		runtime = datetime.strptime(runtime, "%H %M")
		runtime = runtime.strftime("%H:%M:00")	
	else: 
		runtime = None
	#print ("Runtime: " + str(runtime))

	# 7 = Rating

	rating = info[7].getText()
	#print ("Rating: " + rating) 

	# 8 = Production Budget

	budget = info[8].getText()
	if budget != 'N/A':
		budget = re.sub("[$,]", "", budget)
		if 'million' in budget:
			budget = str(int(float(budget.replace ('million', '')) * 1000000))
	else:
		budget = None
	#print ("Budget: " + str(budget))


	with connection.cursor() as cursor:
		sql = (
			"INSERT INTO `movies` (`title`, `release_date`) VALUES (%s, %s) ON DUPLICATE KEY UPDATE `title`=%s, `release_date`=%s"
			)
		#print (sql)
		cursor.execute(sql, (title, release, title, release))
		#print ('Success')
	connection.commit()

	global CURRENT_TITLE
	CURRENT_TITLE = title

def readTableData(url, connection):

	PRIMARY_ID = 1
	
	# print (url)
	tableurl = "http://www.boxofficemojo.com/movies/?page=weekly&id=insertidhere.htm"
	movieid = url[39:-4]
	tableurl = tableurl.replace("=insertidhere", movieid)
	# print (tableurl)

	try:
		with urllib.request.urlopen(tableurl) as response:

			html = response.read()
			#print (html)

		if "NO WEEKLY DATA AVAILABLE" in str(html):
			print ("No Data Available")
			return

		soup = BeautifulSoup(html, 'html.parser')
		#print (soup.prettify().encode('utf-8'))

		# The tables are separated by year, so we need to keep
		# track of the different years each row is about
		yearList = []
		yearIndex = 0
		for font in soup.find_all('font', size="5", face="Verdana"):
			yearInfo = str(font.getText().encode('utf-8')).strip('b').strip("'")
			if len(yearInfo) == 4:
				yearList.append(yearInfo)

		# Set the first year
		year = yearList[yearIndex]

		#print (soup.find_all('table')[2].prettify().encode('utf-8'))
		for tr in soup.find_all('table')[2].find_all('tr')[8:]:

			# Fix a bug where the table row is skipped for some reason
			if 'Date(' in tr.getText():
				yearIndex+=1
				try:
					year = yearList[yearIndex]
				except IndexError:
					year = yearList[yearIndex-1]
				continue

			#print (tr.getText().encode('utf-8'))
			tds = tr.find_all('td')

			# DATE - Encoded weirdly 
			date = str(tds[0].getText().encode('utf-8')).strip('b').strip("'").replace("\\xc2\\x96", " - ") 

			# RANK
			rank = tds[1].getText().strip('b').strip("'").replace(',','')
			if rank == '-':
				rank = None

			# Weekly Gross
			weekly_gross = tds[2].getText().strip('b').strip("'").strip('$').replace(',','').replace('(Estimate)','')

			# Change
			change = tds[3].getText().strip('b').strip("'").replace(',','')
			if change == '-':
				change = '0'

			# Theaters
			theaters = tds[4].getText().strip('b').strip("'").replace(',','')
			if theaters == '-':
				theaters = None

			# Change in Theaters
			change_theaters = tds[5].getText().strip('b').strip("'").replace(',','')
			if change_theaters == '-':
				change_theaters = None

			# Average 
			average = tds[6].getText().strip('b').strip("'").strip('$').replace(',','')
			if average == '-':
				average = None

			# Gross
			gross = tds[7].getText().strip('b').strip("'").strip('$').replace(',','').replace('(Estimate)','')
			if gross == '-':
				gross = None

			# Week
			week = tds[8].getText().strip('b').strip("'")

			print (
				"ID: %s, Title: %s, Year: %s, Date: %s, Rank: %s, Weekly Gross: %s, Change: %s, "
				"Theaters: %s, Change: %s, Average: %s, Gross to date: %s, Week #: %s"
				% (PRIMARY_ID, CURRENT_TITLE, year, date, rank, weekly_gross, change, 
					theaters, change_theaters, average, gross, week))


			with connection.cursor() as cursor:
				sql = (
					"INSERT INTO `time_sensitive` (`id`, `title`, `year`, `date`, `rank`, `weekly_gross`, "
					"`change_wg`, `theaters`, `change_theaters`, `average`, `gross_to_date`, `week`) "
					"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
					"ON DUPLICATE KEY UPDATE `year`=%s, `date`=%s, `rank`=%s, `weekly_gross`=%s, `change_wg`=%s, "
					"`theaters`=%s, `change_theaters`=%s, `average`=%s, `gross_to_date`=%s, `week`=%s"
					)
				#print (sql)
				cursor.execute(sql, (PRIMARY_ID, CURRENT_TITLE, year, date, rank, weekly_gross, 
					change, theaters, change_theaters, average, gross, week, year, date, rank, 
					weekly_gross, change, theaters, change_theaters, average, gross, week))
				# print ('Success')
			connection.commit()

			# Increment primary id
			PRIMARY_ID+=1

	except Exception as e:
		print ("readTableData error " + str(type(e)))
		print (e)
		return


def emptyTable(table):
	connection = pymysql.connect(host = 'localhost', user = 'root',
	password = 'pass', db = 'entertainment_analytics', charset = 'utf8mb4',
	cursorclass = pymysql.cursors.DictCursor) 

	try:
		with connection.cursor() as cursor:
			# Clears the table
			sql = "TRUNCATE `" + table + "`"
			cursor.execute(sql)
		connection.commit()
	finally:
		connection.close()	

if __name__ == '__main__':
	getURLs()
	baseScrapingLoop()