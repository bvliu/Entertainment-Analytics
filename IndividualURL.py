from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import re
from datetime import datetime

# Keep track of primary keys for the time sensitive table
CURRENT_TITLE = ""
PRIMARY_ID = 1


url = "http://www.boxofficemojo.com/movies/?page=weekend&id=starwars7.htm"
with urllib.request.urlopen(url) as response:

	# gets the raw html code from the URL
	html = response.read()
	#print (html)

# Use Beautiful Soup to organize the html into a more readable way
soup = BeautifulSoup(html, 'html.parser')
#print (soup.encode("utf-8"))

# BETTER WAY TO DO IT:
info = soup.find_all('b')

def readStaticData():
	# 1 = title

	title = info[1].getText()
	#print ("Title: " + title)

	# 2 = domestic total as of some date

	total = info[2].getText()
	total = re.sub('[$,]','',total)
	total = int(total)
	#print ("Domestic Total Gross: " + str(total))

	if "Domestic Lifetime Gross" in info[3].getText():
		del info[3]

	# 3 = distributor

	distributor = info[3].getText()
	#print ("Distributor: " + distributor)

	# 4 = release date

	release = info[4].getText()
	try:
		#print ("Release Date: " + release)
		release = re.sub("[,]","",release)
		#print (release)
		release = datetime.strptime(release, "%B %d %Y")
		#print(release.strftime("%Y-%m-%d"))
	except ValueError:
		if len(release) == 4:
			release = release + '-01-01'


	# 5 = Genre

	genre = info[5].getText()
	#print ("Genre: " + genre)

	# 6 = Runtime

	runtime = info[6].getText()
	#print(runtime)
	temp = runtime.split(' ')
	runtime = temp[0] + " " +temp[2]
	runtime = datetime.strptime(runtime, "%H %M")
	runtime = runtime.strftime("%H:%M:00")	

	#print ("Runtime: " + runtime)

	# 7 = Rating

	rating = info[7].getText()
	#print ("Rating: " + rating) 

	# 8 = Production Budget

	budget = info[8].getText()
	#print (budget)
	if budget != 'N/A':
		budget = budget.strip('$')
		budget = str(int(budget.replace ('million', '')) * 1000000)
	#print ("Production Budget: " + budget)

readStaticData()

def readTableData():
	try:
		tableurl = "http://www.boxofficemojo.com/movies/?page=weekend&id=insertidhere.htm"
		movieid = url.strip('.htm').strip("http://www.boxofficemojo.com/movies/?id")
		tableurl = tableurl.replace("=insertidhere", movieid)
		print (tableurl)

		with urllib.request.urlopen(tableurl) as response:

			html = response.read()
			#print (html)

		soup = BeautifulSoup(html, 'html.parser')
		#print (soup.prettify().encode('utf-8'))

		# print (soup.find_all('table')[2].prettify().encode('utf-8'))

		# x = 0
		# for tr in soup.find_all('table')[2].find_all('tr'):
		# 	print (x)
		# 	x+=1
		# 	print(tr.getText().encode('utf-8'))

		yearList = []
		yearIndex = 0
		for font in soup.find_all('font', size="5", face="Verdana"):
			year = str(font.getText().encode('utf-8')).strip('b').strip("'")
			print (year)
			yearList.append(year)

		print (yearList)
		for tr in soup.find_all('table')[2].find_all('tr')[8:]:

			if 'Date(' in tr.getText():
				yearIndex+=1
				year = yearList[yearIndex]
				continue

			tds = tr.find_all('td')
			date = str(tds[0].getText().encode('utf-8')).strip('b').strip("'").replace("\\xc2\\x96", " - ") #date is encoded weirdly
			rank = tds[1].getText().strip('b').strip("'")
			weekend_gross = tds[2].getText().strip('b').strip("'").strip('$')

			change = (tds[3].getText().strip('b').strip("'"))
			if change == '-':
				change = 0

			theaters = tds[4].getText().strip('b').strip("'")

			change_theaters = tds[5].getText().strip('b').strip("'")
			if change_theaters == '-':
				change_theaters = 0

			average = tds[6].getText().strip('b').strip("'").strip('$')
			gross = tds[7].getText().strip('b').strip("'").strip('$')
			week = tds[8].getText().strip('b').strip("'")

			print (
				"ID: %s, Title: %s, Year: %s, Date: %s, Rank: %s, Weekend Gross: %s, Change: %s, "
				"Theaters: %s, Change: %s, Average: %s, Gross to date: %s, Week #: %s"
				% (PRIMARY_ID, CURRENT_TITLE, year, date, rank, weekend_gross, change, 
					theaters, change_theaters, average, gross, week))



	except Exception as e:
		print (type(e))
		print (e)
		return


readTableData()

