#PURPOSE: This will scrape movie contents off of a website (IMDb) 

from bs4 import BeautifulSoup 
import urllib.request
import sys

total=len(sys.argv)
cmdargs=str(sys.argv)

print("total: " + str(total))
print("cmdargs: " + cmdargs)

#Create a .bat file to run and start at various parts of the movie website 
start=int(sys.argv[1])
startFile=sys.argv[2]

#Put in the write mode 'w' (This will drop the output files)
#scrapeIMDb.py will scrape the movies on IMDb to the dummyList text file you create. 
f = open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\' + startFile,'w')

#This error file will capture any errrors that may happen 
errorFile=open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\errorEx.txt','w')

counter=1 

#This will run through the various IMDb pages (100 movies to each page) -> Stops at 1268... continue after. 
for x in range(start,start+1000, 1):
	try: 
		tempURL='http://www.imdb.com/list/ls000344406/?start='
		tempURL+=str(x)
		tempURL+='&view=detail&sort=title:asc'

		r= urllib.request.urlopen(tempURL)
		html=r.read()
		soup=BeautifulSoup(html, "html.parser")
		
		tableStats = soup.find("div", { "class" : "list detail"})

		flag=1

		#This will collect the names of the movies on the website and put them on the text file. 
		for row in tableStats.find_all('a'):
			try:
				name=row.getText()

				print(name)
				name=name.replace("\n","")

				if str(name)=="":
					flag=1

				if flag==1:		
					if str(name)!="":	
						print(name) 
						f.write(name+'\n')
						flag=0	

			except Exception as e: 
				pass
				
		counter+=1 
		print(start)
		start+=1

	except Exception as e: 
		pass

#Goes to the next 100 

f.close
errorFile.close