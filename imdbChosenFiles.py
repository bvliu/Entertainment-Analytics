import urllib.request
import json
from bs4 import BeautifulSoup 
import re
import sys

total=len(sys.argv)
cmdargs=str(sys.argv)

fileSave=sys.argv[1]
fileOpen=sys.argv[2]

x=0

out = open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\Redo\\' + fileSave,'w')
error=open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\errorEx.txt','w')

f=open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\Redo\\' + fileOpen)
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

#START OF THE PRODUCTION COMPANY!!!! -------------------------------------
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

		if str(genres)=="": 
			isUnknown=1

		isOther=1
		isUnknown=0 

		#Genres and the 1/0
		isAction=0 
		if "Action" in genres: 
			isAction=1
			isOther=0

		print(isAction)
		out.write(str(isAction) + "\t")

		isBiography=0 
		if "Biography" in genres:
			isBiography=1 
			isOther=0

		print(isBiography)
		out.write(str(isBiography) + "\t")

		isDocumentary=0 
		if "Documentary" in genres: 
			isDocumentary=1
			isOther=0

		print(isDocumentary)
		out.write(str(isDocumentary) + "\t")

		isFantasy=0 
		if "Fantasy" in genres: 
			isFantasy=1
			isOther=0

		print(isFantasy)
		out.write(str(isFantasy) + "\t")

		isHistory=0 
		if "History" in genres: 
			isHistory=1
			isOther=0

		print(isHistory)
		out.write(str(isHistory) + "\t")

		isMusical=0 
		if "Musical" in genres: 
			isMusical=1
			isOther=0

		print(isMusical)
		out.write(str(isMusical) + "\t")

		isReality=0
		if "Reality-TV" in genres: 
			isReality=1
			isOther=0

		print(isReality)
		out.write(str(isReality) + "\t")

		isSport=0
		if "Sport" in genres: 
			isSport=1
			isOther=0

		print(isSport)
		out.write(str(isSport) + "\t")

		isWar=0
		if "War" in genres: 
			isWar=1
			isOther=0

		print(isWar)
		out.write(str(isWar) + "\t")

		isAdventure=0 
		if "Adventure" in genres: 
			isAdventure=1
			isOther=0

		print(isAdventure)
		out.write(str(isAdventure) + "\t")

		isComedy=0
		if "Comedy" in genres: 
			isComedy=1

		print(isComedy)
		out.write(str(isComedy) + "\t")

		isDrama=0 
		if "Drama" in genres: 
			isDrama=1
			isOther=0

		print(isDrama)
		out.write(str(isDrama) + "\t")

		isFilmNoir=0
		if "Film-Noir" in genres: 
			isFilmNoir=1
			isOther=0

		print(isFilmNoir)
		out.write(str(isFilmNoir) + "\t")

		isHorror=0 
		if "Horror" in genres: 
			isHorror=1
			isOther=0

		print(isHorror)
		out.write(str(isHorror) + "\t")

		isMystery=0 
		if "Mystery" in genres: 
			isMystery=1
			isOther=0

		print(isMystery)
		out.write(str(isMystery) + "\t")

		isRomance=0 
		if "Romance" in genres: 
			isRomance=1
			isOther=0

		print(isRomance)
		out.write(str(isRomance) + "\t")

		isTalk=0
		if "Talk-Show" in genres: 
			isTalk=1
			isOther=0

		print(isTalk)
		out.write(str(isTalk) + "\t")

		isWestern=0 
		if "Western" in genres: 
			isWestern=1
			isOther=0

		print(isWestern)
		out.write(str(isWestern) + "\t")

		isAnimation=0 
		if "Animation" in genres: 
			isAnimation=1
			isOther=0

		print(isAnimation)
		out.write(str(isAnimation) + "\t")
		
		isCrime=0 
		if "Crime" in genres: 
			isCrime=1
			isOther=0

		print(isCrime)
		out.write(str(isCrime) + "\t")

		isFamily=0 
		if "Family" in genres: 
			isFamily=1
			isOther=0

		print(isFamily)
		out.write(str(isFamily) + "\t")

		isGame=0 
		if "Game-Show" in genres: 
			isGame=1
			isOther=0

		print(isGame)
		out.write(str(isGame) + "\t")

		isMusic=0
		if "Music" in genres: 
			isMusic=1
			isOther=0

		print(isMusic)
		out.write(str(isMusic) + "\t")

		isNews=0
		if "News" in genres: 
			isNews=1
			isOther=0

		print(isNews)
		out.write(str(isNews) + "\t")

		isSciFi=0
		if "Sci-Fi" in genres: 
			isSciFi=1
			isOther=0

		print(isSciFi)
		out.write(str(isSciFi) + "\t")

		isThrill=0  
		if "Thriller" in genres: 
			isThrill=1
			isOther=0

		print(isThrill)
		out.write(str(isThrill) + "\t")
		print(isOther)
		out.write(str(isOther) + "\t")
		print(isUnknown)
		out.write(str(isUnknown) + "\t")

#THIS IS THE RATING! ------------------------ 
		urlRating='http://www.imdb.com/title/'
		urlRating+=id
		urlRating+='/ratings?ref_=tt_ov_rt'

		r= urllib.request.urlopen(urlRating)
		html=r.read()
		soup=BeautifulSoup(html, "html.parser")

		tableStats=soup.find("table", { "cellpadding" : "0"})

		for row in tableStats.findAll('tr')[0:]:
			#find all td
			col=row.findAll('td')

			try: 
				out.write(col[1].getText()+"\t") 

			except Exception as e: 
				errorFile.write (str(x) + '************' + str(e) + '*************' + str(col) + '\n') 
				pass 

		#---------------------------------------------------------
		#SECOND TABLE 

		tableStats=soup.findAll("table", { "cellpadding" : "0"})[1]

		for row in tableStats.findAll('tr')[1:]:
			#find all td
			col=row.findAll('td')

			try: 
				#This prints out the number of people 
				print(col[0].getText())
				out.write(col[0].getText() + "\t") 
				#^gets the title
				print(col[1].getText())
				out.write(col[1].getText() + "\t")
				#^gets the number of people
				print(col[2].getText())
				out.write(col[2].getText() + "\t")
				#^gets the rating  

			except Exception as e: 
				errorFile.write (str(x) + '************' + str(e) + '*************' + str(col) + '\n') 
				pass 

	except Exception as e: 
		print("Exception")
		pass

	out.write("\n")
	line=f.readline()

f.close
out.close
error.close

