from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import pymysql.cursors

# ------------------------------------BOX OFFICE MOJO SCRAPER---------------------------------------------

BUDGETS_URL = "http://www.the-numbers.com/movie/budgets/all"

def scrapeMovieBudgets():
	try:
		with urllib.request.urlopen(BUDGETS_URL) as response:
			html = response.read()
	except Exception as e:
		print (type(e) + ": " + e)
		return

	soup = BeautifulSoup(html, 'html.parser')
	print (soup.prettify().encode('utf-8'))

	printRows(soup)

def printRows(soup):	
	for tr in soup.find_all('tr'):
		print (str(tr.getText.encode('utf-8')))
	print ('Finished printing.')

if __name__ == '__main__':
	scrapeMovieBudgets()
