#PURPOSE: This will take the names of the movies and insert them into the OMDb API 

import urllib.request
import json
from bs4 import BeautifulSoup 
import re

x=0

#This will take the movie list, dummyList, and output data onto the rating.txt file. 
out = open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\rating.txt','w')
error=open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\errorEx.txt','w')

f=open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\dummyList.txt')
line=f.readline()

while line: 
	try: 
		line=line.replace("\n","")
		line=line.replace(" ","+")
		line=line.replace("\"","")
		print (line)
		tempURL= 'http://www.omdbapi.com/?t='
		tempURL+=line
		tempURL+='&y=&plot=short&r=json'

		html=urllib.request.urlopen(tempURL)	
		
		#Always put two lines

		text=html.read().decode('utf-8')
		json_obj=json.loads(text)
#------------------------------------------------------------------------
		#These are taken from the OMDb API
		out.write(json_obj['Title']+'\t')
		out.write(json_obj['Year']+'\t')
		out.write(json_obj['Rated']+'\t')
		out.write(json_obj['Released']+'\t')
		out.write(json_obj['Runtime']+'\t') 
		out.write(json_obj['Genre']+'\t')
		out.write(json_obj['Director']+'\t')
		out.write(json_obj['Writer']+'\t')
		out.write(json_obj['Actors']+ "\t") 
		out.write(json_obj['Plot']+ "\t") 
		out.write(json_obj['Language']+'\t')
		out.write(json_obj['Country']+'\t')
		out.write(json_obj['Awards']+'\t')
		out.write(json_obj['Metascore']+ "\t") 
		out.write(json_obj['imdbRating']+ "\t") 
		out.write(json_obj['imdbVotes']+'\t')
		out.write(json_obj['imdbID']+ "\t") 
		out.write(json_obj['Type']+ "\t") 
		
		id=json_obj['imdbID']
		genres=json_obj['Genre']
		genres=genres.replace("\"","")
		print(genres)

#Extra: Production Company findings -------------------------------------
		urlProd="http://www.imdb.com/title/"
		urlProd+=id 
		urlProd+="/companycredits?ref_=tt_dt_co"

		readURL=urllib.request.urlopen(urlProd).read()	
		soup=BeautifulSoup(readURL, "html.parser")
		tableStats=soup.find("ul", { "class" : "simpleList"})

		for row in tableStats.find_all('a'):
			try:
				name=row.getText()
				name=name.replace("\n","")
				out.write(name)

				if "<li>":
					out.write(",")
				print(name)

			except Exception as e: 
				pass

		out.write("\t")

	except Exception as e: 
		print("Exception")
		pass

	out.write("\n")
	line=f.readline()

f.close
out.close
error.close