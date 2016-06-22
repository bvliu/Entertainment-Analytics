#This is a good vid to watch! 
#https://www.youtube.com/watch?v=BCJ4afDX4L4

from bs4 import BeautifulSoup 
import urllib2

f= open("C:\Python27\project\FFootball_DiamonMine\outfileESPN.txt','w')
errorFile=open('C:\Python27\project\FFootball_DiamonMine\outfileESPN.txt','w')

x=0
        
while (x<500): 
        soup=BeautifulSoup(urllib2.urlopen('http://games.espn.go.com/ffl/tools/projections?startIndex='+str(x)).read(), 'html')
        tableStats=soup.find("table", { "class" : "playerTableTable tableBody"})
        
        for row in tableStats.findAll('tr') [2:]:
            col=row.findAll('td')
        
            try: 
                name=col[0].a.string.strip()
                f.write(name+'\n')
        
            except Exception as e: 
                errorFile.writ (str(x) + '************' + str(e) + '*************' + str(col) + '\n') 
                pass 
        
        x=x+40
        
f.close
errorFile.close