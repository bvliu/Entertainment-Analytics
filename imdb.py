import urllib.request
import json

x=0

#html= urllib.request.urlopen('http://www.omdbapi.com/?t=Finding+Dory&y=&plot=short&r=json')

#in = open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\dummyList.txt','r')

out = open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\outfileEx.txt','w')
error=open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\errorEx.txt','w')


f=open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\dummyList.txt')
line=f.readline()

while line: 
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

	try: 
	
		out.write(json_obj['Title']+'\t')
		out.write(json_obj['Year']+'\t')
		out.write(json_obj['Rated']+'\t')
		out.write(json_obj['Genre']+'\t') 
		out.write(json_obj['Awards']+'\t')
		out.write(json_obj['imdbVotes']+'\t')
		out.write(json_obj['imdbRating']+'\t')
		out.write(json_obj['imdbID']+'\n') 

	except Exception as e: 
		errorFile.write(json_obj['Title'])
		pass



	line=f.readline()

f.close() 

out.close
error.close

#Find a way to convert JSON text into python language 
#http://www.omdbapi.com/
