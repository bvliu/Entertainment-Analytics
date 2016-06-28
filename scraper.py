from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse
import urllib.request
import pymysql.cursors
import re

# ------------------------------------BOX OFFICE MOJO SCRAPER---------------------------------------------

#BASE_YEAR = "1980"
BASE_YEAR = "1980"
CURRENT_YEAR = "2016"


# General http address for Box Office Mojo
BOM = "http://www.boxofficemojo.com"

# Iterate through every year
def baseScrapingLoop():

	# Make sure we start off with a blank SQL database CHANGE THIS LATER
	#emptyTable()

	connection = pymysql.connect(host = 'localhost', user = 'root',
	password = 'pass', db = 'test', charset = 'utf8mb4',
	cursorclass = pymysql.cursors.DictCursor) 

	try:
		# Loop through each year starting from the first year (1980) to the current year, set above
		for year in range(int(BASE_YEAR), int(CURRENT_YEAR) + 1):

			# List of the (year) top grossing films, which will be parsed for the URLs
			url = "http://www.boxofficemojo.com/yearly/chart/?page=1&view=releasedate&view2=domestic&yr=1980&p=.htm"
			url = url.replace('yr=1980', 'yr=' + str(year))
			print (str(year))

			# Now, when the “with” statement is executed, Python evaluates the expression, 
			# calls the __enter__ method on the resulting value (which is called a 
			# “context guard”), and assigns whatever __enter__ returns to the variable 
			# given by as. Python will then execute the code body, and no matter what 
			# happens in that code, call the guard object’s __exit__ method.
			with urllib.request.urlopen(url) as response:

				# gets the raw html code from the URL
				html = response.read()
				#print (html)

			# Use Beautiful Soup to organize the html into a more readable way
			soup = BeautifulSoup(html)
			organized = soup.prettify() 	
			#print(organized)	

			scrapeMoviesFromYear(url, connection)

		connection.commit()

	finally:
		connection.close()


# Iterate through each of the individual pages under the year, 0-100 101-200 etc.
def scrapeMoviesFromYear(url, connection):

	# Keep track of the current page
	currentPage = 0

	# Want to find every movie url for the given year
	while True:
		currentPage += 1
		url = url.replace("?page=" + str(currentPage - 1), "?page=" + str(currentPage))
		print (url)
		print (str(currentPage))

		with urllib.request.urlopen(url) as response:	
			html = response.read()

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
				scrapeDataFromMovie(movieurl, connection)


def scrapeDataFromMovie(url, connection):

	#print (url)
	try:
		with urllib.request.urlopen(url) as response:

			# gets the raw html code from the URL
			html = response.read()
			#print (html)

			# Use Beautiful Soup to organize the html into a more readable way
			soup = BeautifulSoup(html, 'html.parser')
			#print (soup.encode("utf-8"))

			readStaticData(soup.find_all('b'), connection)
	except (urllib.error.HTTPError, UnicodeEncodeError, IndexError):
		return

def readStaticData(info, connection):
	# 1 = title

	try:
		title = info[1].getText()
	except IndexError:
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
		sql = ("INSERT INTO `movies` (`title`, `domestic_gross`, `distributor`, "
			"`release_date`, `genre`, `run_time`, `rating`, `production_budget`) " 
			"VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE "
			"`domestic_gross`=%s, `distributor`=%s, `release_date`=%s, `genre`=%s,"
			" `run_time`=%s, `rating`=%s, `production_budget`=%s")
		#print (sql)
		cursor.execute(sql, (title, total, distributor, release, genre, runtime, rating, 
			budget, total, distributor, release, genre, runtime, rating, budget))
		#print ('Success')
	connection.commit()


def emptyTable():
	connection = pymysql.connect(host = 'localhost', user = 'root',
	password = 'pass', db = 'test', charset = 'utf8mb4',
	cursorclass = pymysql.cursors.DictCursor) 

	try:
		with connection.cursor() as cursor:
			# Clears the table
			sql = "TRUNCATE `movies`"
			cursor.execute(sql)
		connection.commit()
	finally:
		connection.close()

baseScrapingLoop()
