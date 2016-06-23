#This is a good vid to watch! 
#https://www.youtube.com/watch?v=BCJ4afDX4L4

from bs4 import BeautifulSoup 
import urllib.request

#This will scrape contents off of a website 

#Put in the write mode 'w' (This will drop the output files)
f = open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\outfileEx.txt','w')

#This error file will capture any errrors that may happen 
errorFile=open('C:\\Users\\582406\\Documents\\Courtney 2016\\DataScrapeExample\\errorEx.txt','w')

x=0

#Gives top 500 

r= urllib.request.urlopen('http://games.espn.go.com/ffl/tools/projections?startIndex=')
html=r.read()

#print (html)

soup=BeautifulSoup(html, "html.parser")

tableStats = soup.find("table", { "class" : "playerTableTable tableBody"})
    
for row in tableStats.findAll('tr') [2:]:
	col=row.findAll('td')
        
	try: 
       		#You want the TEXT of the link (the name or movie title
       		
		name = col[1]
		
		f.write(name.a.getText()+ "\n") 
	

		#One player on each output
                   
	except Exception as e: 
		errorFile.write (str(x) + '************' + str(e) + '*************' + str(col) + '\n') 
		pass
       
x=x+40 
#Goes to the next 40 
        
f.close
errorFile.close
