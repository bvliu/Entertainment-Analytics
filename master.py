import boxofficemojo
import sundance

if __name__ == '__main__':
	
	print ('Running Box Office Mojo')
	boxofficemojo.getURLs()
	boxofficemojo.baseScrapingLoop()

	print ('Running Sundance Scrape')
	sundance.baseScrapingLoop()




