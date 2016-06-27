from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import re
from datetime import datetime

url = "http://www.boxofficemojo.com/movies/?id=willieandphil.htm"
#url = "http://www.boxofficemojo.com/movies/?id=madtiger.htm"

with urllib.request.urlopen(url) as response:

	# gets the raw html code from the URL
	html = response.read()
	#print (html)

# Use Beautiful Soup to organize the html into a more readable way
soup = BeautifulSoup(html, 'html.parser')
#print (soup.encode("utf-8"))

# BETTER WAY TO DO IT:
info = soup.find_all('b')
x = 0
for item in info:
	print (item.encode('utf-8'))
	print (str(x) + " " + item.getText())
	x+=1

def readStaticData():
	# 1 = title

	title = info[1].getText()
	print ("Title: " + title)

	# 2 = domestic total as of some date

	total = info[2].getText()
	total = re.sub('[$,]','',total)
	total = int(total)
	print ("Domestic Total Gross: " + str(total))

	if "Domestic Lifetime Gross" in info[3].getText():
		del info[3]

	# 3 = distributor

	distributor = info[3].getText()
	print ("Distributor: " + distributor)

	# 4 = release date

	release = info[4].getText()
	try:
		print ("Release Date: " + release)
		release = re.sub("[,]","",release)
		print (release)
		release = datetime.strptime(release, "%B %d %Y")
		print(release.strftime("%Y-%m-%d"))
	except ValueError:
		if len(release) == 4:
			release = release + '-01-01'


	# 5 = Genre

	genre = info[5].getText()
	print ("Genre: " + genre)

	# 6 = Runtime

	runtime = info[6].getText()
	print(runtime)
	temp = runtime.split(' ')
	runtime = temp[0] + " " +temp[2]
	runtime = datetime.strptime(runtime, "%H %M")
	runtime = runtime.strftime("%H:%M:00")	

	print ("Runtime: " + runtime)

	# 7 = Rating

	rating = info[7].getText()
	print ("Rating: " + rating) 

	# 8 = Production Budget

	budget = info[8].getText()
	print (budget)
	if budget != 'N/A':
		budget = budget.strip('$')
		budget = str(int(budget.replace ('million', '')) * 1000000)
	print ("Production Budget: " + budget)

readStaticData()

