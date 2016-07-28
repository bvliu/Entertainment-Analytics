import urllib.request
import json
from bs4 import BeautifulSoup 
import re

x=0

#out = open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\testing7-24.txt','w')
out = open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\Redo\\ProAndRating\\list2.txt','w')

error=open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\errorEx.txt','w')

f=open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\Redo\\MovieListPart1.txt')
line=f.readline()

while line: 

	mVotes=0
	avM=0.0
	feVotes=0
	avFe=0.0

	check1=0
	avCheck1=0.0
	mCheck1=0
	avMCheck1=0.0
	feCheck1=0
	avFeCheck1=0.0
	
	check2=0
	avCheck2=0.0
	mCheck2=0
	avMCheck2=0.0
	feCheck2=0
	avFeCheck2=0.0
	
	check3=0
	avCheck3=0.0
	mCheck3=0
	avMCheck3=0.0
	feCheck3=0
	avFeCheck3=0.0

	check4=0
	avCheck4=0.0
	mCheck4=0
	avMCheck4=0.0
	feCheck4=0
	avFeCheck4=0.0

	US=0
	avUS=0.0
	nonUS=0
	avNonUS=0.0

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
		
		title=json_obj['Title']
		out.write(title + "\t")
		id=json_obj['imdbID']
		out.write(id+"\t")

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

#THIS IS THE RATING! ------------------------ 

		urlRating='http://www.imdb.com/title/'
		urlRating+=id
		urlRating+='/ratings?ref_=tt_ov_rt'

		r= urllib.request.urlopen(urlRating)
		html=r.read()
		soup=BeautifulSoup(html, "html.parser")

		tableStats=soup.find("table", { "cellpadding" : "0"})
	

		for row in tableStats.findAll('tr'):
			#find all td
			col=row.findAll('td')
			
			out.write(col[1].getText() + "\t")

		#Ratings 1-10 

		#---------------------------------------------------------
		#SECOND TABLE 

		tableStats=soup.findAll("table", { "cellpadding" : "0"})[1]

		for row in tableStats.findAll('tr'):

			col=row.findAll('td')
			words=col[0].getText()
			num=col[1].getText()
			average=col[2].getText()

			words=words.strip(' \t\n\r')
			
			print("Start:" + words)
			print("Number:" + num)
			print("Average:" + average)

			if words=="Males": 
				mVotes=num
				avM=average
			
			if words== "Females": 
				feVotes=num
				avFe=average

			if words== "Aged under 18": 
				check1=num
				avCheck1=average

			if words=="Males under 18": 
				mCheck1=num
				avMCheck1=average
			
			if words== "Females under 18": 
				feCheck1=num
				avFeCheck1=average
			
			if words== "Aged 18-29": 
				check2=num
				avCheck2=average
			
			if words== "Males Aged 18-29": 
				mCheck2=num
				avMCheck2=average
			
			if words== "Females Aged 18-29": 
				feCheck2=num
				avFeCheck2=average
			
			if words== "Aged 30-44": 
				check3=num
				avCheck3=average
			
			if words== "Males Aged 30-44": 
				mCheck3=num
				avMCheck3=average
			
			if words== "Females Aged 30-44": 
				feCheck3=num
				avFeCheck3=average

			if words== "Aged 45+": 
				check4=num
				avCheck4=average
			
			if words== "Males Aged 45+": 
				mCheck4=num
				avMCheck4=average
			
			if words== "Females Aged 45+": 
				feCheck4=num
				avFeCheck4=average

			if words== "US users": 
				US=num
				avUS=average
			
			if words== "Non-US users": 
				nonUS=num
				avNonUS=average

			print("Average Males Start: " + str(avM))
			print("Words End: " + words + "\n")
	
	except Exception as e: 
		print("\n")
		pass

	print("Average Males: " + str(avM))	
	out.write(str(mVotes) + "\t" + str(avM) + "\t" + str(feVotes)+ "\t" + str(avFe)+ "\t" + str(check1)+ "\t" + str(avCheck1)+ "\t" + str(mCheck1)+ "\t" + str(avMCheck1) + "\t" + str(feCheck1) + "\t" + str(avFeCheck1)+ "\t"	+ str(check2)+ "\t" + str(avCheck2)+ "\t" + str(mCheck2)+ "\t" + str(mCheck2)+ "\t" + str(avMCheck2)+ "\t" + str(feCheck2)+ "\t" + str(avFeCheck2)+ "\t" + str(check3)+ "\t" + str(avCheck3)+ "\t" + str(mCheck3)+ "\t" + str(avMCheck3)+ "\t" + str(feCheck3)+ "\t" + str(avFeCheck3)+ "\t" + str(check4)+ "\t"+ str(avCheck4)+ "\t"+ str(mCheck4)+ "\t" + str(avMCheck4)+ "\t"+ str(feCheck4)+ "\t"+ str(avFeCheck4)+ "\t"+ str(US)+ "\t"+ str(avUS)+ "\t"+ str(nonUS) + "\t"+ str(avNonUS) + "\n")
	line=f.readline()

f.close
out.close
error.close