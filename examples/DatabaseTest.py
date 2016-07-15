import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host = 'localhost', user = 'root', password = 'pass', db = 'test', charset = 'utf8mb4', 
	cursorclass = pymysql.cursors.DictCursor)

try:
 	with connection.cursor() as cursor:
 		sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
 		cursor.execute(sql, ('webmaster@python.org', 'very-secret'))	

 	connection.commit()
 		
 	with connection.cursor() as cursor:
 		sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
 		cursor.execute(sql, ('webmaster@python.org',))
 		result = cursor.fetchone()
 		print(result)

finally:
 	connection.close()