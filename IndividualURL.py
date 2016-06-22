from bs4 import BeautifulSoup
import urllib.parse
import urllib.request

url = "http://www.boxofficemojo.com/movies/?id=horsemoney.htm"
#url = "http://www.boxofficemojo.com/yearly/chart/?page=1&view=releasedate&view2=domestic&yr=2015&p=.htm"

with urllib.request.urlopen(url) as response:

	# gets the raw html code from the URL
	html = response.read()
	#print (html)

# Use Beautiful Soup to organize the html into a more readable way
soup = BeautifulSoup(html, 'html.parser')


# TITLE -----------------------------------------------------------------
title = soup.title.getText()

#print(title.find(" - Box Office Mojo")) --> 18
#print(title[:18]) but still has the parentheses

# Slice from the beginning of the parentheses
title = title[:title.find(" (")]
print (title)

# BUDGET ----------------------------------------------------------------

print (soup.find_all("b")[3].getText())