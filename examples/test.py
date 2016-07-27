import re
from datetime import *

def formatTime(myTime)
	runtime = int(myTime.replace(' min', ''))

	minutes = runtime%60
	hours = runtime//60

	runtime = str(hours) + ' ' + str(minutes)

	runtime = datetime.strptime(runtime, "%H %M")
	runtime = runtime.strftime("%H:%M:00")	
	return runtime
