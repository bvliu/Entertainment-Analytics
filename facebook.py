import requests
import json
import urllib.request
import urllib.parse
import pymysql
import time
import datetime
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from urllib.parse import urlencode
import csv

appid = "1118759701501012"
appsecret = "0ad3fbde533a3e4662f36a86389e7764"
# access_token="1118759701501012|x2pLWmhjDhSD3RbTG-qs_VyyNtE"

#appid = "1566084017029348"
#appsecret = "9ac4952612861e3aa65de0c6e4b81060"
access_token= appid + "|" + appsecret

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
	connection = pymysql.connect(host = 'localhost', user = 'root',
	password = 'pass', db = 'entertainment_analytics', charset = 'utf8mb4',
	cursorclass = pymysql.cursors.DictCursor) 

	with connection.cursor() as cursor:
		sql = "SELECT m.`id`, `title`, `release_date` FROM `movies` as m LEFT OUTER JOIN `facebook` as f ON (m.`id` = f.`id`) WHERE f.`id` IS NULL"
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
    if not data:
    	return (None, None, None)
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
	tries = 0
	while success is False:
		print ('trying ' + str(tries) + " - " + url)
		tries+=1
		try:
			data = requests.get(url)
			if data.status_code == 200:
				success = True
			elif data.status_code == 500:
				print ('Internal Service error 500: ' + url)
				return
			elif 'error' in data.json():
				if data.json()['error']['code'] == 4:
					continue
				print ('Error ' + url)
				return

		except Exception as e:
			print (e)
			time.sleep(5)
			print ('Error for URL %s: %s' % (url, datetime.datetime.now()))
	return data.json()

queryList = getTitles()
for x in queryList:
	print (x)
POOL.map(scrapeDataFromPage, [x for x in queryList])