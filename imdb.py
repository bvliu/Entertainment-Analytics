import urllib.request
import json
from bs4 import BeautifulSoup 

#pymysql.connect 

x=0

out = open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\outfileEx.txt','w')
error=open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\errorEx.txt','w')

f=open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\dummyList.txt')
line=f.readline()

while line: 
	try: 
		line=line.replace("\n","")
		line=line.replace(" ","+")
		print (line)
		tempURL= 'http://www.omdbapi.com/?t='
		tempURL+=line
		tempURL+='&y=&plot=short&r=json'

		html=urllib.request.urlopen(tempURL)	
		
		#Always put two lines

		text=html.read().decode('utf-8')
		json_obj=json.loads(text)
#--------------------------------
		out.write(json_obj['Title']+'\t')
		out.write(json_obj['Year']+'\t')
		out.write(json_obj['Rated']+'\t')
		out.write(json_obj['Genre']+'\t') 
		out.write(json_obj['Awards']+'\t')
		out.write(json_obj['imdbVotes']+'\t')
		out.write(json_obj['imdbRating']+'\t')
		out.write(json_obj['imdbID']+ "\t") 

		id=json_obj['imdbID']
		#sets the id for later - prodIMDb.py 

		url2="http://www.imdb.com/title/"
		url2+=id 
		url2+="/companycredits?ref_=tt_dt_co"

		
		readURL=urllib.request.urlopen(url2).read()	

		soup=BeautifulSoup(readURL, "html.parser")

		tableStats=soup.find("ul", { "class" : "simpleList"})


		for row in tableStats.find_all('a'):

			#***just testing *** 
	
			try:
				name=row.getText()
				name=name.replace("\n","")
				out.write(name + ",")
				print(name)

			except Exception as e: 
				pass

		out.write("\n")

	except Exception as e: 
		print("Exception")
		pass

	line=f.readline()

f.close() 
out.close
error.close
