import re
from datetime import *


def formatDate(release):
	try:
		release = re.sub("[,]", "", release)
		release = datetime.strptime(release, "%d %b %Y")
		release = release.strftime("%Y-%m-%d")
	except ValueError:
		if release == 'N/A': # If the date format is N/A
			release = None
		elif len(release) == 4: # If the date format is only the year
			release = release + '-01-01'
		elif len(release) > 4: # If the date format is the month then the year (June 1981)
			release = datetime.strptime(release, "%B %Y")
			release = release.strftime("%Y-%m-01")
	print ("Release Date: " + str(release))
	return release

print (formatDate('02 Nov 1999'))