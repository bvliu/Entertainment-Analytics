from bs4 import BeautifulSoup
import urllib.parse
import urllib.request

url = "http://www.boxofficemojo.com/yearly/chart/?yr=2000&p=.htm"
bom = "http://www.boxofficemojo.com"

with urllib.request.urlopen(url) as response:
# Now, when the “with” statement is executed, Python evaluates the expression, 
# calls the __enter__ method on the resulting value (which is called a 
# “coxntext guard”), and assigns whatever __enter__ returns to the variable 
# given by as. Python will then execute the code body, and no matter what 
# happens in that code, call the guard object’s __exit__ method.

	html = response.read()
	#gets the URL
	#print (html)

#print (html)
soup = BeautifulSoup(html)
organized = soup.prettify() 	
print(organized)

def getURLs(soup):
# Return a list of the URLs
	urls = []
	for link in soup.find_all('a'):
		name = str(link.get('href'))
		if 'movies' in name and 'ref=ft' not in name:
			urls.append(bom + name)
	print(urls)
getURLs(soup)
