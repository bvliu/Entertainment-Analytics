from bs4 import BeautifulSoup
import urllib.parse
import urllib.request

# List of the 2015 top grossing films, which will be parsed for the URLs
url = "http://www.boxofficemojo.com/yearly/chart/?yr=2015&p=.htm"

# General http address for Box Office Mojo
bom = "http://www.boxofficemojo.com"

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

# Return a list of the movie URLs
def getMovieURLs(soup):

	# Create the list
	urls = []

	# Search the soup for the <a tag that precedes all href links
	for link in soup.find_all('a'):
		name = str(link.get('href'))

		# if movies is in the link then it's the one we're looking for,
		# not ref = ft is a special case that we don't want to be in the list
		if 'movies' in name and 'ref=ft' not in name: 
			urls.append(bom + name) # Add it to the list, maybe should do some sorting here?
	print(urls)

getMovieURLs(soup)
