import urllib.request
import json

x=0

html= urllib.request.urlopen('http://www.omdbapi.com/?t=Finding+Dory&y=&plot=short&r=json')

print(html)

#Always put two lines

text=html.read().decode('utf-8')
json_obj=json.loads(text)

#--------------------------------

print(json_obj['Title'])
print(json_obj['imdbRating'])
#Or you can print to a text file
#Next step... loop?  

#Find a way to convert JSON text into python language 
#http://www.omdbapi.com/