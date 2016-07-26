import requests
import json
import urllib.request
import urllib.parse
import pymysql
import time
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from urllib.parse import urlencode
import csv

appid = "1118759701501012"
appsecret = "0ad3fbde533a3e4662f36a86389e7764"
access_token="1118759701501012|x2pLWmhjDhSD3RbTG-qs_VyyNtE"

POOL = Pool(cpu_count()*2)


def generateQueryString(title):
	base = "https://graph.facebook.com/v2.7/search/?access_token=%s" % access_token
	fields = '&fields=fan_count,is_verified'
	params = {"q": title}
	query_string = '&' + urllib.parse.urlencode(params)
	# print (base+'&type=page'+query_string+fields)
	return base+'&type=page'+query_string+fields


def getTitles(): 
	queryList = []
	connection = pymysql.connect(host = '10.201.31.179', user = 'fooUser',
	password = 'pass', db = 'imdb', charset = 'utf8mb4',
	cursorclass = pymysql.cursors.DictCursor) 

	with connection.cursor() as cursor:
		sql = "SELECT `id`, `title`, `release_date` FROM `movies`"
		cursor.execute(sql)
		for row in cursor:
			movieID = row['id']
			title = row['title']
			date = row['release_date']
			queryList.append((generateQueryString(title + ' movie'), str(movieID)))

	connection.commit()
	connection.close()

	return queryList

# Returns (is_verified, fb_id, fan_count)
def scrapeDataFromPage(info):
	url = info[0]
	movieID = info[1]
	connection = pymysql.connect(host = 'localhost', user = 'root',
	password = 'pass', db = 'entertainment_analytics', charset = 'utf8mb4',
	cursorclass = pymysql.cursors.DictCursor) 

	try:
		with connection.cursor() as cursor:
			(verified, fbID, likes) = performScrape(url)
			print (str(verified) + " " + str(fbID) + " " + str(likes))
			sql = (
				"INSERT INTO `facebook` (`id`, `fb_id`, `verified`, `likes`) VALUES "
				"(%s, %s, %s, %s) ON DUPLICATE KEY UPDATE `fb_id`=%s, `verified`=%s, `likes`=%s"
				)
			cursor.execute(sql, (movieID, fbID, verified, likes, fbID, verified, likes))
		connection.commit()
	except json.decoder.JSONDecodeError as e:
		print ('JSON Decode Error')
	finally:
		connection.close()

def performScrape(url):
    data = requestUntilSucceed(url)
    if not data['data']:
    	return (None, None, None)
    else:
    	foundVerified = False
    	for row in data['data']:
    		if row['is_verified'] == True:
    			foundVerified = True
    			return ('true',str(row['id']), str(row['fan_count']))
    	return ('false', str(data['data'][0]['id']), str(data['data'][0]['fan_count']))


def requestUntilSucceed(url):
	success = False
	while success is False:
		try:
			data = requests.get(url)
			if data.status_code == 200:
				success = True
		except Exception as e:
			print (e)
			time.sleep(5)
			print ('Error for URL %s: %s' % (url, datetime.datetime.now()))
	return data.json()

queryList = getTitles()
for x in queryList:
	print (x)
POOL.map(scrapeDataFromPage, [x for x in queryList])