from bs4 import BeautifulSoup 
import urllib.request

#This will scrape contents off of a website 

#Put in the write mode 'w' (This will drop the output files)
f = open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\dummyList.txt','w')

#This error file will capture any errrors that may happen 
errorFile=open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\errorEx.txt','w')

for x in range(1,1268, 100):
	tempURL='http://www.imdb.com/list/ls000344406/?start='
	tempURL+=str(x)
	tempURL+='&view=detail&sort=title:asc'

	r= urllib.request.urlopen(tempURL)

	html=r.read()

	soup=BeautifulSoup(html, "html.parser")
	tableStats = soup.find("div", { "class" : "list detail"})

	flag=1

	for row in tableStats.find_all('a'):

		try:
			name=row.getText()
			#Prints Pulp Fiction

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

#Goes to the next 100 

f.close
errorFile.close