#This is a good vid to watch! 
#https://www.youtube.com/watch?v=BCJ4afDX4L4

#*****Still working on this file to change the example to get movie titles*****

from bs4 import BeautifulSoup 
import urllib2

#This will scrape contents off of a website 

#Put in the write mode 'w' (This will drop the output files)
f = open('C:\Documents\Courtney 2016\DataScrapeExample\outfileEx.txt','w')

#This error file will capture any errrors that may happen 
errorFile=open('C:\Documents\Courtney 2016\DataScrapeExample\errorEx.txt','w')

x=0

#Gives top 500 
while (x<500): 
    soup=BeautifulSoup(urllib2.urlopen('http://games.espn.go.com/ffl/tools/projections?startIndex='+str(x)).read(), 'html')
   
    #On the html page, you will find the <table> tag 
    tableStats = soup.find("table", { "class" : "playerTableTable tableBody"})
    
    for row in tableStats.findAll('tr') [2:]:
        col=row.findAll('td')
        
        try: 
            #You want the TEXT of the link (the name or movie title)
            name = col[0].a.string.strip()
            f.write(name+'\n') #One player on each output
        
        #str(x) row 
        #str(e) output exception
        #When it hits the exception, log it then continue 
                    
            except Exception as e: 
                errorFile.write (str(x) + '************' + str(e) + '*************' + str(col) + '\n') 
                pass
        
        x=x+40 #Goes to the next 40 
        
f.close
errorFile.close
